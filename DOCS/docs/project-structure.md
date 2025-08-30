# 📂 Project Structure

This document explains the internal structure of **Vultrix**.  
It helps developers understand the role of each module, making it easier to contribute or extend the project.

---

## 🗂 Root Folder

```

Vultrix\_Open\_Source/
│
├── requirements.txt        ← Python requirements (dependencies)
├── DOCS/          ← Documentation files (markdown)
├── .gitignore     ← Git ignore rules
├── LICENSE        ← License file (MIT)
└── Program/       ← Main application source code

```

---

## 🖥 Program Folder

```

Program/
├── index.py                ← Application entry point
├── core/                   ← Core app logic
├── Data/                   ← Data management & APIs
├── AppData/                ← Local app data/config (e.g. \~/.vultrix/)
├── Styles/                 ← Themes & visual styling
├── trading\_charts/         ← Charting modules
└── web\_pages/              ← GUI pages

```

---

## ⚙️ Core Modules (`Program/core/`)

- **utils.py** → General helper functions (math, conversions, formatting).  
- **show_sharts.py** → Functions to render/display charts.  
- **open_program.py** → Handles opening/closing and main app runtime.  
- **window.py** → GUI window management.  
- **shart_classes.py** → Chart classes and models (candles, depth, etc.).  

---

## 📡 Data Layer (`Program/Data/`)

- **cypher.py** → Encryption / decryption for user data (API keys, passwords).  
- **api.py** → REST/WebSocket wrappers for Binance & other exchanges.  
- **logs.py** → Logging system (errors, runtime messages).  
- **utils.py** → Data-related utilities (conversions, formatting).  
- **user_data.py** → Manage user registration, login, and saved settings.  

---

## 🗃 AppData (`Program/AppData/`)

- Stores application data/config.  
- In the official app, this lives in:  
```
\~/.vultrix/
```

---

## 🎨 Styles (`Program/Styles/`)

- **binance_plot_them.py** → Binance-style chart theme (colors, fonts, etc.).  

---

## 📈 Trading Charts (`Program/trading_charts/`)

- **candels_shart.py** → Candlestick chart logic.  
- **utils.py** → Helper functions for chart plotting.  

---

## 🌐 Web Pages (`Program/web_pages/`)

- **home.py** → Home page of the app.  
- **wallet.py** → Wallet page (balances, funds).  
- **pup_messages.py** → Popup messages (alerts, errors, warnings).  
- **errors.py** → Error handling pages/UI.  

---

## 📦 Plugins (External)

- Plugins are mounted from:
```
\~/.vultrix/Plugins/
```

- Only `.zip` plugins are supported.  
- Plugin Manager is **closed-source** in this edition.  

---

## 📝 Summary

- **Core** → The engine of Vultrix (charts, windows, logic).  
- **Data** → APIs, encryption, user info, logs.  
- **Styles** → Themes and appearance.  
- **Trading Charts** → Actual chart drawing and utilities.  
- **Web Pages** → GUI pages for the user interface.  
- **AppData** → Local configs and saved data.  
- **Plugins** → External features, loaded separately.  

This modular structure makes it easy to extend Vultrix with new features while keeping code organized.