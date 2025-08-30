# 👨‍💻 Developer Overview

Welcome to the **Vultrix Developer Documentation**.  
This section explains the internal structure of the codebase to help contributors understand, extend, and maintain the project.

---

## 🔑 Key Concepts
- **Core Layer** → Main logic & utilities (window management, chart classes).  
- **Data Layer** → APIs, encryption, user storage, and logging.  
- **Charting Layer** → Handles candlestick and depth chart rendering.  
- **UI Layer** → Web pages & GUI windows.  
- **Entry Point** → `index.py` bootstraps the app and connects all layers.  

---

## 📂 High-Level Architecture

```

index.py (Entry Point)
│
├── core/           → Core logic & GUI management
├── Data/           → APIs, user data, security, logs
├── trading\_charts/ → Charting utilities
└── web\_pages/      → GUI Pages

```

---

## 📚 Table of Contents

### 1. 📂 Project Structure
- [Project Structure](./project-structure.md)

### 2. ⚙️ Core System
- [Core Modules](./core_modules.md)

### 3. 🗂️ Data Layer
- [Data Modules](./data_modules.md)

### 4. 📊 Charting Engine
- [Trading Charts](./charts_modules.md)

### 5. 🌐 GUI Pages
- [Web Pages](./web-pages_modules.md)

### 6. 🚀 Application Entry
- [Index Entry Point](./index_entry_point.md)

---

## ⚙️ Developer Notes
- All modules follow **modular design**: each file has a clear role.  
- Keep **separation of concerns**:  
  - Data handling → `Data/`  
  - Visualization → `trading_charts/`  
  - GUI → `web_pages/`  
- Core modules act as the **bridge** between Data Layer and UI Layer.  
- Future: a unified **Plugin Manager API** will be added (currently closed-source).  

---

## 📌 Contribution Guidelines
- Document your functions with **docstrings**.  
- Use **type hints** where possible.  
- Keep the architecture modular: do not mix UI logic with data logic.  