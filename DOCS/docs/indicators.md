# 📊 Indicators

Vultrix provides different types of indicators for cryptocurrency market analysis.  
Some indicators are **open-source** (included in this repository), while others are **closed-source plugins** distributed separately.

---

## ✅ Open-Source Indicators

These indicators are included in the project by default:

- **Moving Average (MA)**  
  - Simple trend-following indicator.  
  - Helps smooth price action to identify direction.

- **Candlestick Chart Tools**  
  - Standard crypto chart visualization.  
  - Includes support for different intervals (1m, 5m, 1h, 1d, …).  

*(More open indicators may be added in the future — see [Roadmap](../ROADMAP.md)).*  

---

## 🔒 Closed-Source Indicators (Plugins)

These advanced indicators are **not part of the open-source repository** 
They are provided as **separate proprietary plugins**:

- **Volume HeatMap**  
  - Visual representation of market liquidity.  
  - Highlights clusters of high volume at specific price levels.  

- **Cumulative Volume Delta (CVD)**  
  - Measures the difference between buying and selling pressure.  
  - Helps to identify market imbalances.  

- **Other Proprietary Indicators**  
  - May include advanced order flow and market depth tools.  
  - Released as paid or private plugins.  

⚠️ **Note**: Closed-source plugins are not covered by the MIT license of this project.  

---

## 🛠 How to Use Indicators

1. Open **Charts Window**.  
2. Choose your trading pair (example: `BTCUSDT`).  
3. Select an indicator from the **Indicators menu**.  
4. Click **Add** → The indicator will be applied to the chart.  

---

## 📌 Notes

- Using too many indicators at once may slow down performance due to **Binance API limits**.  
- Closed-source plugins require separate installation and are not available in this repository.  
- For custom indicator development, see [Contributing Guide](../CONTRIBUTING.md).  
