# 🔗 Binance API Integration

Vultrix integrates directly with the **Binance Exchange API** to fetch real-time and historical market data.  
It uses both **REST APIs** (for snapshot data) and **WebSocket streams** (for live updates).  

---

## 📦 Authentication

- Public endpoints (e.g., Order Book, Trades, Klines) do **not** require authentication.  
- Private endpoints (e.g., Account Info, Wallet Balances) require:  
  - **API Key** (HMAC SHA256)  
  - **Secret Key**  

⚠️ Store your keys securely. Vultrix encrypts sensitive user data via `Program/Data/cypher.py`.  

---

## 📡 REST API (Snapshot Data)

These are **HTTP GET requests** to Binance’s API.  
Vultrix uses them for initial data snapshots.

### 🔍 Endpoints

- **Order Book (Depth of Market)**
    ```http
    GET /api/v3/depth?symbol=BTCUSDT&limit=100
    ```

* **Recent Trades**

  ```http
  GET /api/v3/trades?symbol=BTCUSDT&limit=500
  ```

* **Klines / Candlesticks**

  ```http
  GET /api/v3/klines?symbol=BTCUSDT&interval=1m&startTime=...&endTime=...
  ```

* **Average Price**

  ```http
  GET /api/v3/avgPrice?symbol=BTCUSDT
  ```

📚 Official Docs → [Binance REST API](https://binance-docs.github.io/apidocs/spot/en/#public-rest-api)

---

## 📡 WebSocket API (Real-Time Data)

WebSocket streams provide **continuous live updates** (low latency).
Vultrix relies on them to keep charts and indicators in sync.

### 🔍 Streams

* **Depth Stream (Diff updates)**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@depth
  ```

* **Partial Depth (levels 5, 10, 20)**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@depth10@100ms
  ```

* **Trades**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@trade
  ```

* **Aggregate Trades**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@aggTrade
  ```

* **Candlestick (Kline)**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@kline_1m
  ```

* **Average Price**

  ```
  wss://stream.binance.com:9443/ws/btcusdt@avgPrice
  ```

📚 Official Docs → [Binance WebSocket API](https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams)

---

## ⚙️ How Vultrix Uses Binance API

* **Order Book** → DOM visualization (price walls, liquidity).
* **Trades & CVD** → Order flow analysis.
* **Volume HeatMap** (closed-source plugin) → Liquidity clusters.
* **Candlesticks** → Chart rendering (with indicators).

---

## ⚠️ Rate Limits

Binance enforces strict API rate limits:

* REST: 1200 requests / minute (default).
* WebSocket: Too many subscriptions may trigger disconnects.

👉 Vultrix uses **async programming** (`asyncio`) to stay efficient and within limits.

---

## 🛡️ Best Practices

* Always test with **small intervals** first (e.g., 1m Klines).
* Cache REST results and rely on WebSocket for live sync.
* Use only the **symbols you need** (avoid opening too many streams).
* Keep your **API keys private** (never commit them to GitHub).

---

## 📌 Summary

* **REST API** → Snapshots (Order Book, Trades, Klines, Avg Price).
* **WebSocket API** → Live updates (Depth, Trades, Candles).
* Vultrix integrates both to power real-time trading visualizations.
* Closed-source indicators (like HeatMap & CVD) depend heavily on Binance WebSocket streams.