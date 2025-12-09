import requests
import pandas as pd
import time
import json

def fetch_all_stocks():
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    page = 1
    page_size = 100
    all_stocks = []
    
    print("Fetching stock list from Sina Finance...")
    
    while True:
        params = {
            "page": page,
            "num": page_size,
            "sort": "symbol",
            "asc": 1,
            "node": "hs_a",
            "symbol": "",
            "_s_r_a": "page"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}")
                break
                
            data = response.json()
            
            if not data:
                break
                
            for item in data:
                symbol = item.get('symbol', '')
                code = item.get('code', '')
                name = item.get('name', '')
                
                # Filter for SH and SZ stocks
                # Sina returns symbols like sh600000, sz000001, bj...
                if symbol.startswith('sh') or symbol.startswith('sz'):
                    # Format code as 600000.SH or 000001.SZ
                    market = symbol[:2].upper()
                    formatted_code = f"{code}.{market}"
                    
                    all_stocks.append({
                        "code": formatted_code,
                        "name": name,
                        "symbol": symbol
                    })
            
            print(f"Fetched page {page}, total stocks so far: {len(all_stocks)}")
            page += 1
            time.sleep(0.5) # Be nice to the API
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    df = pd.DataFrame(all_stocks)
    df.to_csv("all_stocks.csv", index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} stocks to all_stocks.csv")
    return df

if __name__ == "__main__":
    fetch_all_stocks()
