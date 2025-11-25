# 请求协议以及响应格式

## 1、HTTP请求协议以及响应协议

### 1.1、请求头

所有HTTP接口均为`GET`请求，需要在请求头`Headers`里面固定设置您的API Key

我的API key是 28222a4f7c7c4ae6bfe07d8bb75cfc82-infoway

### 1.2、响应格式

```
{
    "ret": 200,
    "msg": "success",
    "traceId": "698f920a-c53b-401c-bfac-4ea46b9b8f12",
    "data": [
        
    ]
}
```

字段:描述
ret:响应码。200为正常响应（错误码）
msg:success
tradeId:由系统生成的唯一ID
data:响应数据返回

## 2、Websocket

所有类型的WebSocket连接，地址相同，仅参数不同，详情请看[Websocket订阅地址说明](https://docs.infoway.io/websocket-api/endpoints)和[Websocket代码示例](https://docs.infoway.io/websocket-api/code-examples)。
