import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Set page config
st.set_page_config(page_title="A股实时行情看板", layout="wide")

st.title("A股实时行情看板")

# Sidebar for configuration
st.sidebar.header("设置")
# Default API Token from documentation
DEFAULT_TOKEN = "28222a4f7c7c4ae6bfe07d8bb75cfc82-infoway"
api_token = st.sidebar.text_input("API Token", value=DEFAULT_TOKEN, type="password", help="请输入您的 API Token")
stock_code = st.sidebar.text_input("股票代码", value="600519", help="例如: 600519 (贵州茅台), 00700 (腾讯), AAPL (苹果)")
region = st.sidebar.selectbox("市场", ["cn", "hk", "us"], index=0, help="cn: A股, hk: 港股, us: 美股")

# Timeframe selection
timeframe_map = {
    "1分钟": 1,
    "5分钟": 2,
    "15分钟": 3,
    "30分钟": 4,
    "1小时": 5,
    "日K": 8,
    "周K": 9,
    "月K": 10
}
selected_timeframe = st.sidebar.selectbox("K线周期", list(timeframe_map.keys()), index=5) # Default to Daily (index 5)
kline_type = timeframe_map[selected_timeframe]

# API Base URL
BASE_URL = "https://data.infoway.io/stock"

def format_code(code, region):
    code = code.strip().upper()
    if region == "cn":
        # If user already entered suffix, trust it but ensure uppercase
        if code.endswith(".SH") or code.endswith(".SZ") or code.endswith(".SS"):
            return code.replace(".SS", ".SH") # Normalize SS to SH if needed, though API seems to accept SH
        
        # Auto-append suffix based on common rules
        if code.startswith("6"):
            return f"{code}.SH"
        if code.startswith("0") or code.startswith("3"):
            return f"{code}.SZ"
        if code.startswith("8") or code.startswith("4"): # Beijing Stock Exchange usually
             return f"{code}.BJ"
        
        return f"{code}.SH" # Default fallback
    elif region == "hk":
        if code.endswith(".HK"):
            return code
        return f"{code}.HK"
    elif region == "us":
        if code.endswith(".US"):
            return code
        return f"{code}.US"
    return code

def get_quote(code, token):
    """Fetch real-time quote data (latest trade)."""
    url = f"{BASE_URL}/batch_trade/{code}"
    headers = {"apikey": token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {e}")
        return None

def get_kline(code, token, k_type):
    """Fetch K-line data."""
    # Fetch 500 candles (enough for ~2 years of daily data or ~8 hours of 1-min data)
    url = f"{BASE_URL}/batch_kline/{k_type}/500/{code}"
    headers = {"apikey": token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {e}")
        return None

if st.button("获取行情"):
    if not api_token:
        st.warning("请先输入 API Token")
    else:
        formatted_code = format_code(stock_code, region)
        with st.spinner(f"正在获取 {formatted_code} 数据..."):
            # Fetch Quote
            quote_data = get_quote(formatted_code, api_token)
            
            if quote_data and quote_data.get("ret") == 200:
                # Display Quote
                st.subheader(f"实时行情: {formatted_code}")
                
                data_list = quote_data.get("data", [])
                if data_list:
                    item = data_list[0]
                    col1, col2, col3, col4 = st.columns(4)
                    
                    price = item.get("p", "N/A")
                    volume = item.get("v", "N/A")
                    turnover = item.get("vw", "N/A")
                    time_ts = item.get("t", 0)
                    
                    # Convert timestamp to readable string (CST)
                    if time_ts:
                        dt_utc = datetime.utcfromtimestamp(time_ts/1000)
                        dt_cst = dt_utc + pd.Timedelta(hours=8)
                        time_str = dt_cst.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        time_str = "N/A"

                    col1.metric("当前价格", price)
                    col2.metric("成交量 (手/股)", volume)
                    col3.metric("成交额", turnover)
                    col4.metric("更新时间", time_str)
                    
                    # st.json(item) # Debug
                else:
                    st.warning("未获取到有效行情数据")
                    st.json(quote_data)
            else:
                st.error("获取行情失败")
                if quote_data:
                    st.json(quote_data)

            # Fetch K-line
            kline_data = get_kline(formatted_code, api_token, kline_type)
            if kline_data and kline_data.get("ret") == 200:
                st.subheader(f"K线走势 ({selected_timeframe})")
                
                data_list = kline_data.get("data", [])
                if data_list:
                    k_item = data_list[0]
                    candles = k_item.get("respList", [])
                    
                    if candles:
                        df = pd.DataFrame(candles)
                        # Rename columns: t, o, h, l, c, v
                        df = df.rename(columns={
                            "t": "time",
                            "o": "open",
                            "h": "high",
                            "l": "low",
                            "c": "close",
                            "v": "volume"
                        })
                        
                        # Convert types
                        # Convert timestamp to China Standard Time (UTC+8)
                        df['time'] = pd.to_datetime(df['time'].astype(int), unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
                        # Remove timezone info to make it naive (wall clock time) for Plotly rangebreaks
                        df['time'] = df['time'].dt.tz_localize(None)
                        
                        df['open'] = df['open'].astype(float)
                        df['high'] = df['high'].astype(float)
                        df['low'] = df['low'].astype(float)
                        df['close'] = df['close'].astype(float)
                        
                        # Sort by time
                        df = df.sort_values('time')

                        # Calculate Moving Averages
                        df['ma5'] = df['close'].rolling(window=5).mean()
                        df['ma10'] = df['close'].rolling(window=10).mean()
                        df['ma20'] = df['close'].rolling(window=20).mean()

                        # Create subplots: Row 1 for Candlestick & MA, Row 2 for Volume
                        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                            vertical_spacing=0.05, 
                                            row_heights=[0.7, 0.3])

                        # Add Candlestick
                        fig.add_trace(go.Candlestick(x=df['time'],
                                        open=df['open'],
                                        high=df['high'],
                                        low=df['low'],
                                        close=df['close'],
                                        name='K线',
                                        increasing_line_color='red',
                                        decreasing_line_color='green'), row=1, col=1)
                        
                        # Add Moving Averages
                        fig.add_trace(go.Scatter(x=df['time'], y=df['ma5'], line=dict(color='orange', width=1), name='MA5'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=df['time'], y=df['ma10'], line=dict(color='blue', width=1), name='MA10'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=df['time'], y=df['ma20'], line=dict(color='purple', width=1), name='MA20'), row=1, col=1)

                        # Add Volume
                        # Color volume bars: Red if Close >= Open, Green if Close < Open
                        vol_colors = ['red' if c >= o else 'green' for o, c in zip(df['open'], df['close'])]
                        fig.add_trace(go.Bar(x=df['time'], y=df['volume'], marker_color=vol_colors, name='成交量'), row=2, col=1)
                        
                        # Configure layout
                        layout_args = dict(xaxis_rangeslider_visible=False, height=600, showlegend=True)
                        
                        # Add rangebreaks for A-shares (CN) to skip non-trading hours
                        if region == "cn":
                            rangebreaks = []
                            # Only apply intraday breaks for minute/hour data
                            if "分钟" in selected_timeframe or "小时" in selected_timeframe:
                                rangebreaks.append(dict(bounds=[11.5, 13], pattern="hour")) # Lunch break 11:30-13:00
                                rangebreaks.append(dict(bounds=[15, 9.5], pattern="hour"))  # Overnight 15:00-09:30
                                rangebreaks.append(dict(bounds=["sat", "mon"])) # Weekends
                            elif selected_timeframe == "日K":
                                rangebreaks.append(dict(bounds=["sat", "mon"])) # Weekends for daily chart
                            
                            if rangebreaks:
                                layout_args['xaxis'] = dict(rangebreaks=rangebreaks)
                        
                        fig.update_layout(**layout_args)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("暂无K线数据")
                else:
                    st.info("暂无K线数据")
            else:
                st.error("获取K线失败")
                if kline_data:
                    st.json(kline_data)

st.markdown("---")
st.markdown("API 来源: [infoway.io](https://data.infoway.io)")
