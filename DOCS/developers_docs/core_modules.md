# ⚙️ Core Modules

Path: `Program/core/`

The **Core Layer** is the backbone of Vultrix.  
It connects the **Data Layer** with the **UI Layer**, manages windows, and provides charting logic.

---

## 📂 Files

### 🛠️ utils.py
- Provides **general helper functions** used across the app.  
- Ensures code reusability and avoids duplication.  
- Contains mathematical helpers, formatting tools, and small wrappers.

**Developer Note:**  
Whenever you need a common function, check here before writing new code.  

---

### 📊 show_sharts.py
- Handles **chart rendering** inside the GUI window.  
- Takes market data from `Data/api.py` and sends it to visualization.  
- Communicates with `shart_classes.py` to decide what chart to show.

**Workflow:**
1. Fetches market data.  
2. Chooses chart class (candlestick, DOM, etc.).  
3. Displays chart inside the app window.  

---

### 🚀 open_program.py
- Responsible for **bootstrapping** the app.  
- Prepares initial configurations, environment, and user settings.  
- Acts as the first step before window rendering.  

**Tasks:**
- Load user preferences.  
- Initialize default settings.  
- Launch `window.py`.  

---

### 🖼️ window.py
- Manages **GUI windows** for Vultrix.  
- Handles user interactions like:
  - Opening/closing windows.  
  - Resizing and layout.  
  - Navigation between pages.  

**Developer Note:**  
All GUI logic should be here → avoid mixing with charting or API code.  

---

### 📈 shart_classes.py
- Defines **chart classes** used for different trading views:  
  - Candlestick charts  
  - Depth of Market (DOM)  
  - Volume charts  

- Provides **OOP abstraction** → each chart type is a class.  

**Example:**  
```python
class CandlestickChart:
    def __init__(...):
        ...
    def render(self):
        ...
```

---

## 🧭 Flow Between Modules

1. `index.py` calls **open\_program.py**.
2. `open_program.py` loads configs & calls **window\.py**.
3. When a user opens a chart:

   * **show\_sharts.py** fetches data (from `Data/`).
   * **shart\_classes.py** decides how to render it.
   * Chart is displayed inside the **window**.

---

## 📝 Developer Notes

* **Keep separation of concerns**:

  * `window.py` → only GUI.
  * `shart_classes.py` → only chart definitions.
  * `show_sharts.py` → glue code between data & charts.

* Always reuse `utils.py` for helper functions.

* Core Modules are critical → test them carefully after changes.