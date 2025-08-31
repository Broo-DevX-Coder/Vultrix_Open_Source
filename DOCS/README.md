# ⚠️ Disclaimer
This project is **open-source** and developed **solely for educational and experimental purposes**.  
Any misuse is strictly prohibited. In particular:

- ❌ Engaging in pump-and-dump schemes or trading tokens questionable under Islamic law (Shariah).  
- ❌ Using this project for futures trading, leveraged trading, or other high-risk financial instruments.  
- ❌ Employing this tool in unregulated or illegal markets.  

The author assumes **no responsibility** for any misuse or violations of legal, ethical, or religious standards.  
Users are responsible for ensuring compliance with **local laws**, **exchange policies**, and **religious guidelines**.  

---

# 📖 Overview

## Project Info
- **Name**: Vultrix  
- **Status**: 🚧 In Development  
- **Version**: 0.1.0.mvp
- **Description**:  
  > Vultrix is a charting and indicator platform for cryptocurrency markets.  
  > Unlike traditional tools like *MetaTrader* or *TradingView*, it is a standalone application offering features such as **Volume Maps** and **Depth of Market (DOM)** visualization.
- **Note**
  > _Closed-Source_ Plugins never work out of the official app

---

## 📚 Documentation


  - [Contributing](./CONTRIBUTING.md)
  - [Licence](../LICENSE)
  - [Islamic Licence](./LICENCE_ISLAMIC.md)
  - [Roadmap](./ROADMAP.md)
  - [Installation](./docs/installation.md)
  - [Usage Guide](./docs/usage.md)
  - [Indicators](./docs/indicators.md)

for More Info, view our wiki: [Wiki Home](https://github.com/Broo-DevX-Coder/Vultrix_Open_Source/wiki)

---

## 🔧 Tech Stack
- **Python** → Core programming language  
- **Async Programming** → Efficient event-driven concurrency  
- **REST APIs** → Market data from centralized exchanges (Binance, Bitget, …)  
- **WebSockets** → Real-time price and order book streams  
- **Pandas** → DataFrames and preprocessing  
- **NumPy** → Fast numerical computations  
- **Matplotlib** → Visual chart rendering inside the GUI  
- **PySide2 / PyQtGraph / qasync** → GUI and charting integration  

---

## 📂 Project Structure

```

Vultrix\_Open\_Source/
│
├── requirements.txt  ← Requirement file
├── DOCS/             ← Documentation folder
├── .gitignore        ← For GitHub
├── LICENSE           ← MIT License
│
├── Program/
│    ├── index.py          ← Entry point
│    ├── core/
│    │    ├── utils.py
│    │    ├── show\_sharts.py
│    │    ├── open\_program.py
│    │    ├── window\.py
│    │    └── shart\_classes.py
│    ├── Data/
│    │    ├── cypher.py
│    │    ├── api.py
│    │    ├── logs.py
│    │    ├── utils.py
│    │    └── user\_data.py
│    ├── AppData/           ← In official app, stored in `~/.vultrix`
│    ├── Styles/
│    │    └── binance\_plot\_them.py
│    ├── trading\_charts/
│    │    ├── candels\_shart.py
│    │    └── utils.py
│    └── web\_pages/
│         ├── home.py
│         ├── wallet.py
│         ├── pup\_messages.py
│         └── errors.py

```

---

## 🚀 Installation and Setup

1. Clone the repository  
   ```bash
   git clone https://github.com/Broo-DevX-Coder/Vultrix_Open_Source.git
   ```

2. Install dependencies

   ```bash
   cd ./Vultrix_Open_Source
   pip install -r requirements.txt
   ```

3. Run the application

   ```bash
   cd Program
   python index.py
   ```

---

## 🖥️ Usage

1. Run the program:

   ```bash
   python index.py
   ```

2. Options:

   * **Register & Login** → Add your info:

     * Username
     * Binance API Key (HMAC SHA256)
     * Binance Secret Key
     * Ciphering password + confirmation
   * **Continue without Login** → Direct access to charting tools only.

3. Once logged in, open the **Charts** window (last icon in the toolbar).

4. Set any symbol (e.g., `BTCUSDT`), add an indicator (e.g., Moving Average), and click **Add**.

5. You can add unlimited charts — but be mindful of **Binance API limits**.

---

## 📊 Trading Data

* **Order Book (Depth of Market)** → Price walls & market imbalances
* **Market Volume** → Market trend confirmation & structural analysis

---

## 🔗 Binance API Integration

### REST API

* Order Book → `GET /api/v3/depth?symbol=SYMBOL&limit=...`
* Recent Trades → `GET /api/v3/trades?symbol=SYMBOL&limit=...`
* Candlesticks → `GET /api/v3/klines?symbol=SYMBOL&interval=...`
* Average Price → `GET /api/v3/avgPrice?symbol=SYMBOL`

### WebSocket

* Depth Stream → `<symbol>@depth`
* Partial Depth → `<symbol>@depth5`, `<symbol>@depth10`
* Trades → `<symbol>@trade`
* Aggregate Trades → `<symbol>@aggTrade`
* Candlestick → `<symbol>@kline_<interval>`
* Average Price → `<symbol>@avgPrice`

📚 See [Binance API Documentation](https://binance-docs.github.io/apidocs/)

---

## 📜 License

This project is licensed under the **MIT License**.
Closed-source indicators (plugins) are distributed separately and **not covered by this license**.
