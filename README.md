# A股实时行情看板

这是一个基于 Streamlit 的 A股实时行情看板，使用 `api.itick.org` 提供的 API 获取数据。

## 准备工作

1.  **获取 API Token**: 您需要从数据提供商处获取 API Token。
2.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

## 运行看板

在终端中运行以下命令启动应用：

```bash
streamlit run dashboard.py
```

## 功能

-   **实时行情**: 输入股票代码（如 `600519`）查看实时价格、涨跌幅等信息。
-   **K线图**: 查看股票的历史 K 线走势。
-   **多市场支持**: 支持 A股 (cn)、港股 (hk)、美股 (us)。

## 注意事项

-   请确保网络能够访问 `api.infoway.org`。
-   如果 API 返回 401 错误，请检查 Token 是否正确。
