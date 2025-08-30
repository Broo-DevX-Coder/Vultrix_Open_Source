# 🚀 Index Entry Point

File: `Program/index.py`

The **Index Entry Point** is the **main launcher** of Vultrix.  
It is responsible for initializing the environment, loading configurations, and starting the GUI.

---

## 🧩 Responsibilities
- Acts as the **entry point** for the entire application.  
- Imports **core modules** and **web pages**.  
- Initializes logging, API clients, and encryption systems.  
- Starts the main window (`core/window.py`).  

---

## 🛠️ Workflow

1. **Startup**
   - Runs when executing:
     ```bash
     python index.py
     ```
   - Prepares environment variables.  
   - Loads requirements from `req.txt`.  

2. **Initialization**
   - Calls `core/open_program.py` to setup defaults.  
   - Loads user settings and encrypted API keys from `Data/user_data.py`.  
   - Initializes logging (`Data/logs.py`).  

3. **GUI Launch**
   - Starts the main window (`core/window.py`).  
   - Loads the **Home Page** (`web_pages/home.py`).  

4. **Event Handling**
   - When the user requests a chart:
     - `core/show_sharts.py` is triggered.  
     - Fetches data via `Data/api.py`.  
     - Renders chart via `trading_charts/candels_shart.py`.  
   - Handles errors with `web_pages/errors.py`.  
   - Shows notifications via `web_pages/pup_messages.py`.  

---

## 🔗 Example Run Command

```bash
cd Program
python index.py   # or python3 index.py
```

---

## 📝 Developer Notes

* `index.py` should remain **minimal and clean** → only bootstrap code.
* Heavy logic belongs to respective modules (`core/`, `Data/`, `trading_charts/`).
* Good practice: wrap startup code in a `main()` function for clarity.
* If adding new modules, always register them in `index.py`.