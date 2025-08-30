# 📊 Trading Charts Modules

Path: `Program/trading_charts/`

The **Trading Charts Layer** is responsible for rendering and managing trading-related visualizations.  
It transforms raw market data (from Binance API via `Data/api.py`) into interactive financial charts.

---

## 📂 Files

### 🕯️ candels_shart.py
- Implements **candlestick chart rendering**.  
- Uses **Matplotlib** to plot OHLC (Open, High, Low, Close) data.  
- Accepts data fetched from `Data/api.py` (klines / candlesticks).  
- Provides chart updates in near real-time using WebSocket streams.  

**Responsibilities:**
- Convert Binance kline data into visual candlestick plots.  
- Support multiple timeframes (1m, 5m, 1h, etc.).  
- Highlight key features (e.g., volume, trend direction).  

**Developer Note:**  
Candlestick rendering should be optimized to avoid GUI lag when handling high-frequency data.  

---

### 🛠️ utils.py
- Provides **helper functions** for charting logic.  
- Common tasks:  
  - Formatting timestamps.  
  - Calculating moving averages.  
  - Preparing data arrays for Matplotlib.  
  - Converting API responses into plotting structures.  

**Example responsibilities:**
- Convert `{"open": ..., "close": ...}` into an OHLC tuple.  
- Smooth out data series before plotting.  
- Provide shared functions between candlestick and other chart modules.  

---

## 🧭 Flow Between Modules
1. Market data fetched via `Data/api.py`.  
2. Data preprocessed with `trading_charts/utils.py`.  
3. `candels_shart.py` receives cleaned OHLC data.  
4. Chart rendered inside GUI window via `core/show_sharts.py`.  
5. User can add indicators (moving averages, volume, etc.) on top.  

---

## 📝 Developer Notes
- Keep **chart rendering lightweight** → avoid blocking the main GUI thread.  
- All time calculations should be handled in `utils.py`, not in chart classes.  
- Future extensions: footprint charts, volume profiles, and advanced indicators.  
