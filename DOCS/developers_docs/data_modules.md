# 🗂️ Data Modules

Path: `Program/Data/`

The **Data Layer** in Vultrix is responsible for **fetching, securing, and storing data**.  
It handles APIs, cryptography, user information, and logging.

---

## 📂 Files

### 🔐 cypher.py
- Provides encryption/decryption functions.  
- Used to secure sensitive user information (like API keys, passwords).  
- Likely uses a cipher method (AES or Fernet) with a user-provided password.  
- Ensures that even local storage in `AppData/` is not readable in plain text.

**Example responsibilities:**
- Encrypt user data before saving it.  
- Decrypt when loading it for the session.  

---

### 🌐 api.py
- Responsible for handling **external APIs** (mainly Binance for now).  
- Supports both **REST** and **WebSocket** connections.  
- Provides functions to fetch:
  - Order Book depth  
  - Trades  
  - Candlestick (kline) data  
  - Average prices  

**Workflow:**
1. REST requests → fetch historical data.  
2. WebSocket → subscribe for real-time updates.  
3. Forward data to chart modules (`trading_charts/`).  

---

### 📝 logs.py
- Handles logging system events.  
- Creates logs for:
  - Errors (API failures, bad plugins).  
  - Warnings (rate limits, missing configs).  
  - Info (successful connections, user actions).  

**Developer Note:**  
Keeping logs is essential for debugging and user support. Logs are usually stored in a text file inside `AppData/`.

---

### 👤 user_data.py
- Manages user-specific data:
  - Username  
  - Binance API Key (HMAC-SHA256)  
  - Secret Key  
  - Encrypted passwords (via `cypher.py`)  

**Process:**
1. User registers / logs in → info saved securely.  
2. Sensitive keys are encrypted before storage.  
3. On login → data is decrypted and reloaded.  

---

## 🧭 Flow Between Modules
1. User enters credentials → `user_data.py` saves them securely.  
2. Credentials are encrypted using `cypher.py`.  
3. API calls to Binance go through `api.py`.  
4. Any issues/errors are logged in `logs.py`.  
5. Trading data is then forwarded to the **charting modules** for visualization.  

---

## 📝 Developer Notes
- **Never** log raw API keys or passwords → always obfuscate or redact in `logs.py`.  
- Always use `cypher.py` functions when dealing with sensitive data.  
- Respect Binance API limits → avoid excessive calls in `api.py`.  
