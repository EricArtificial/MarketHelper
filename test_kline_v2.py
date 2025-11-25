import requests

BASE_URL = "https://data.infoway.io/stock/v2/batch_kline"
TOKEN = "28222a4f7c7c4ae6bfe07d8bb75cfc82-infoway"
CODE = "600519.SH"

types_to_test = [1, 5, 15, 30, 60, 101, 1440]

for t in types_to_test:
    headers = {
        "apikey": TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "klineType": t,
        "klineNum": 2,
        "codes": CODE
    }
    try:
        response = requests.post(BASE_URL, json=data, headers=headers)
        print(f"Type: {t}, Status: {response.status_code}, Response: {response.text[:100]}")
    except Exception as e:
        print(f"Type: {t}, Error: {e}")
