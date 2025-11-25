import json
import time
import schedule
import threading
import websocket
from loguru import logger

class WebsocketExample:
    def __init__(self):
        self.session = None
        self.ws_url = "wss://data.infoway.io/ws?business=crypto&apikey=yourApikey"
        self.reconnecting = False
        self.is_ws_connected = False  # 添加连接状态标志

    def connect_all(self):
        """建立WebSocket连接并启动自动重连机制"""
        try:
            self.connect(self.ws_url)
            self.start_reconnection(self.ws_url)
        except Exception as e:
            logger.error(f"Failed to connect to {self.ws_url}: {str(e)}")

    def start_reconnection(self, url):
        """启动定时重连检查"""
        def check_connection():
            if not self.is_connected():
                logger.debug("Reconnection attempt...")
                self.connect(url)
        
        # 使用线程定期检查连接状态
        schedule.every(10).seconds.do(check_connection)
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)
        threading.Thread(target=run_scheduler, daemon=True).start()

    def is_connected(self):
        """检查WebSocket连接状态"""
        return self.session and self.is_ws_connected

    def connect(self, url):
        """建立WebSocket连接"""
        try:
            if self.is_connected():
                self.session.close()
            
            self.session = websocket.WebSocketApp(
                url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # 启动WebSocket连接（非阻塞模式）
            threading.Thread(target=self.session.run_forever, daemon=True).start()
        except Exception as e:
            logger.error(f"Failed to connect to the server: {str(e)}")

    def on_open(self, ws):
        """WebSocket连接建立成功后的回调"""
        logger.info(f"Connection opened")
        self.is_ws_connected = True  # 设置连接状态为True
        
        try:
            # 发送实时成交明细订阅请求
            trade_send_obj = {
                "code": 10000,
                "trace": "01213e9d-90a0-426e-a380-ebed633cba7a",
                "data": {"codes": "BTCUSDT"}
            }
            self.send_message(trade_send_obj)
            
            # 不同请求之间间隔一段时间
            time.sleep(5)
            
            # 发送实时盘口数据订阅请求
            depth_send_obj = {
                "code": 10003,
                "trace": "01213e9d-90a0-426e-a380-ebed633cba7a",
                "data": {"codes": "BTCUSDT"}
            }
            self.send_message(depth_send_obj)
            
            # 不同请求之间间隔一段时间
            time.sleep(5)
            
            # 发送实时K线数据订阅请求
            kline_data = {
                "arr": [
                    {
                        "type": 1,
                        "codes": "BTCUSDT"
                    }
                ]
            }
            kline_send_obj = {
                "code": 10006,
                "trace": "01213e9d-90a0-426e-a380-ebed633cba7a",
                "data": kline_data
            }
            self.send_message(kline_send_obj)
            
            # 启动定时心跳任务
            schedule.every(30).seconds.do(self.ping)
            
        except Exception as e:
            logger.error(f"Error sending initial messages: {str(e)}")

    def on_message(self, ws, message):
        """接收消息的回调"""
        try:
            logger.info(f"Message received: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭的回调"""
        logger.info(f"Connection closed: {close_status_code} - {close_msg}")
        self.is_ws_connected = False  # 设置连接状态为False

    def on_error(self, ws, error):
        """错误处理的回调"""
        logger.error(f"WebSocket error: {str(error)}")
        self.is_ws_connected = False  # 发生错误时设置连接状态为False

    def send_message(self, message_obj):
        """发送消息到WebSocket服务器"""
        if self.is_connected():
            try:
                self.session.send(json.dumps(message_obj))
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
        else:
            logger.warning("Cannot send message: Not connected")

    def ping(self):
        """发送心跳包"""
        ping_obj = {
            "code": 10010,
            "trace": "01213e9d-90a0-426e-a380-ebed633cba7a"
        }
        self.send_message(ping_obj)

# 使用示例
if __name__ == "__main__":
    ws_client = WebsocketExample()
    ws_client.connect_all()
    
    # 保持主线程运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting...")
        if ws_client.is_connected():
            ws_client.session.close()