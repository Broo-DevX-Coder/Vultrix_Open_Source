# 🌐 Web Pages Modules

Path: `Program/web_pages/`

The **Web Pages Layer** represents the **GUI sections** of Vultrix.  
Each file defines a page or component that the user can interact with inside the app.

---

## 📂 Files

### 🏠 home.py
- The **main landing page** of Vultrix.  
- Displays general market info, user status, and navigation shortcuts.  
- Acts as the starting point after login / or "continue without login".  

**Responsibilities:**
- Show quick market overview (basic data).  
- Provide navigation buttons to other modules (Charts, Wallet, etc.).  
- Handle user login status (logged in / guest mode).  

---

### 👛 wallet.py
- Manages the **Wallet page** in the GUI.  
- Displays user balance (via API if logged in).  
- Handles viewing of assets and transaction history.  

**Responsibilities:**
- Fetch wallet data from exchange APIs (if API keys provided).  
- Render balances in an easy-to-read table.  
- (Future) Add support for multiple exchanges.  

---

### 💬 pup_messages.py
- Handles **popup messages** (notifications) inside the GUI.  
- Examples:  
  - "Plugin loaded successfully"  
  - "Error: API key missing"  
  - "Connection lost"  

**Responsibilities:**
- Show temporary popup notifications.  
- Handle error alerts and user confirmations.  
- Provide non-intrusive feedback to the user.  

---

### ⚠️ errors.py
- Dedicated page/module for **error handling**.  
- When something fails (bad API call, plugin crash), this module provides a clean error screen.  

**Responsibilities:**
- Show critical error messages with context.  
- Offer guidance (e.g., "Check your API keys" / "Remove invalid plugin").  
- Log errors (in cooperation with `Data/logs.py`).  

---

## 🧭 Flow Between Modules
1. User enters the app → **home.py** is displayed.  
2. If the user opens **Wallet** → `wallet.py` fetches and shows balances.  
3. If an error occurs (bad plugin, API down) → `errors.py` page is triggered.  
4. For smaller notifications (success/failure) → `pup_messages.py` shows a popup without leaving the page.  

---

## 📝 Developer Notes
- Always use **pup_messages.py** for small UI alerts instead of blocking the whole window.  
- Critical issues must redirect to **errors.py** with context.  
- Keep GUI pages **lightweight**: they should fetch data via APIs, not handle logic directly.  
