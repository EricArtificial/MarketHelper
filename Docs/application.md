# GET查询产品列表

## 接口说明

该接口是获取不同市场的产品列表，方便您确认是否包含您所需的产品数据

## 请求频率

跟其他接口请求频率使用同一个频率限制。具体每秒请求次数根据套餐决定。可以参考[接口限制说明](https://docs.infoway.io/getting-started/api-limitation)

## 错误码说明

参考[HTTP错误码说明]：
HTTP错误码
HTTP API接口错误码说明

错误码
说明
503

K线查询数量超出限制

505

产品数量超出限制

508

查询的产品不存在，或已经退市

401

认证错误，API Key不正确，或者未将API Key放置在指定header或query中

404

API接口不存在

429

请求频率限制，请求不符合您当前套餐配额

499

客户端主动中断，通常发生在网络不稳定的地区，请在良好网络环境连接

524

源服务器连接超时，通常发生在我们加速代理提供商到我们服务器之间不稳定导致，一般很快就能恢复

WebSocket错误码
Websocket错误码说明

错误码
说明
500

服务异常

501

请求频率超出一分钟限制

505

产品数量超出限制

506

参数缺失

515

参数不是json格式

513

WebSocket心跳超时

401

认证错误，API Key不正确，或者未将API Key放置在指定header或query中

404

API接口不存在

427

WebSocket连接数量超过套餐配额

429

请求频率限制，请求不符合您当前套餐配额

499

客户端主动中断，通常发生在网络不稳定的地区，请在良好网络环境连接

524

源服务器连接超时，通常发生在我们加速代理提供商到我们服务器之间不稳定导致，一般很快就能恢复

## 接口地址

* 基本路径：`/common/basic/symbols`
* 完整路径：`https://data.infoway.io
  /common/basic/symbols`

## 请求头

| 参数       | 类型     | 必填 | 描述           |
| -------- | ------ | -- | ------------ |
| `apiKey` | String | 是  | 您套餐中的API Key |

## Request param入参说明

| 参数名       | 类型     | 必填 | 描述                                               | 示例值                |
| --------- | ------ | -- | ------------------------------------------------ | ------------------ |
| `type`    | String | 是  | 标的类型，参考下面<mark style="color:blue;">type类型</mark> | `STOCK_US`         |
| `symbols` | String | 否  | 标的列表，多个用,隔开                                      | `.DJI.US,.IXIC.US` |

#### type说明

| 类型代码       | 描述   |
| ---------- | ---- |
| `STOCK_US` | 美股   |
| `STOCK_CN` | A股   |
| `STOCK_HK` | 港股   |
| `FUTURES`  | 期货   |
| `FOREX`    | 外汇   |
| `ENERGY`   | 能源   |
| `METAL`    | 金属   |
| `CRYPTO`   | 加密货币 |

## 返回示例

```json
{
  "ret": 200,
  "msg": "success",
  "traceId": "ed8a84d9-4575-4077-bc1c-31b17d0c8977",
  "data": [
    {
      "symbol": ".DJI.US",
      "name_cn": "道琼斯指数",
      "name_hk": "道瓊斯指數",
      "name_en": "Dow Jones Industrial Average"
    },
    {
      "symbol": ".IXIC.US",
      "name_cn": "纳斯达克综合指数",
      "name_hk": "納斯達克綜合指數",
      "name_en": "NASDAQ Composite Index"
    }
  ]
}
```

| 字段名       | 类型     | 必填 | 描述   | 示例值          |
| --------- | ------ | -- | ---- | ------------ |
| `symbol`  | String | 是  | 标的代码 | `AAPL.US`    |
| `name_cn` | String | 否  | 中文名称 | `苹果`         |
| `name_hk` | String | 否  | 繁体名称 | `蘋果`         |
| `name_en` | String | 否  | 英文名称 | `Apple Inc.` |
