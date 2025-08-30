# 🚀 Installation Guide

This document explains how to install and set up **Vultrix** on your system.

---

## ✅ Requirements

Before installing, make sure you have:

- **Python 3.9+** (recommended: 3.10)  
- **pip** (Python package manager)  
- Internet connection (to fetch data from Binance API)  

Optional but recommended:
- A **Binance account** and **API keys** (for full features).

---

## 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/Broo-DevX-Coder/Vultrix_Open_Source.git
cd Vultrix_Open_Source
```

---

## 📦 Step 2: Install Dependencies

We provide a `requirements.txt` file with all needed Python libraries.

```bash
pip install -r requirements.txt
```

Dependencies include:

* PySide2 (GUI framework)
* PyQtGraph (charting)
* qasync (async integration for Qt)
* numpy, pandas, matplotlib (data handling & visualization)
* httpx, aiohttp, websockets (API & real-time data)
* pycryptodome (security & encryption)

---

## ▶️ Step 3: Run the Program

Go into the `Program/` folder and start the app:

```bash
cd Program
python index.py
```

---

## 🔑 (Optional) Binance API Keys Setup

Some features (like Depth of Market & Volume Map) require Binance API keys.

1. Go to your Binance account → **API Management**.
2. Create a new API key (with read-only permissions).
3. Add your API Key & Secret in the **Register** form when starting Vultrix.

⚠️ **Important**: Do not share your API keys with anyone!

---

## 🎉 Done!

You should now see the **Vultrix Main Window**.

* If you register → full access to charts, indicators, and wallet.
* If you skip login → you can still view charts in demo mode.