# 🖥️ Usage Guide

This document explains how to use **Vultrix** after installation.  

---

## ▶️ Starting the Program

1. Go into the **Program/** folder:
    ```bash
    cd Program
    ```

2. Run the app:

   ```bash
   python index.py
   ```

You should now see the **Vultrix main window**.

---

## 🔑 Login & Registration

When you start the program, you have two options:

### Option 1 → Register & Login

* Enter your:

  * **Username**
  * **Binance API Key (HMAC SHA256)**
  * **Binance Secret Key**
  * **Ciphering Password & Confirmation**
* After registration, you will have **full access**:

  * Volume Maps
  * Depth of Market (DOM)
  * Wallet panel
  * Saved settings

### Option 2 → Continue without Login

* Click **“Continue without Login”**
* You can still access **basic charts** and indicators in demo mode.

---

## 📊 Using Charts

1. Open the **Charts window** (last icon in the toolbar).
2. Choose a trading pair (example: `BTCUSDT`).
3. (Optional) Add an indicator, e.g. *Moving Average*, then click **Add**.
4. Click **“Add Chart”** → a new chart will appear.

⚠️ You can add unlimited charts, but **Binance API has rate limits**.
Be mindful when adding too many charts at once.

---

## 📈 Indicators

* Built-in indicators (e.g., Moving Average) are available in the GUI.
* Advanced/closed-source plugins (e.g., *VolumeHeatMap*, *CVD*) are not included in the open-source release.

---

## ⚠️ Notes

* If Binance API keys are not provided, only **demo features** will work.
* Errors (e.g., connection issues, invalid keys) will be shown in the **popup messages panel**.
* Logs are stored in `Program/Data/logs.py` for debugging.

---

## 🔌 Mounting Plugins

Vultrix supports external **plugins** (advanced indicators, etc.).  
Currently, the **Plugin Manager** is **closed-source**, so only official plugins can be mounted.

### 📁 Plugin Path

All plugins `.zip` files must be placed in:

```
\~/.vultrix/Plugins/
```

- On **Linux/macOS** → `/home/<user>/.vultrix/Plugins/`  
- On **Windows** → `C:\Users\<user>\.vultrix\Plugins\`  

*(This path is resolved internally using `Path.home()/.vultrix/Plugins`).*

---

### 📦 Mounting a Plugin (.zip)

1. Obtain the plugin package (e.g., `VolumeHeatMap.zip`).  
2. Copy the `.zip` file **directly** into the Plugins folder:
```
\~/.vultrix/Plugins/VolumeHeatMap.zip
\~/.vultrix/Plugins/CVD.zip
```
3. Restart Vultrix → the closed-source **Plugin Manager** will automatically load the plugin.  

---

### ⚠️ Important Notes

- **Do not unzip** the file — the system expects plugins as `.zip` archives.  
- **Only official plugins** should be copied.  
- ⚠️ If you copy any unsupported or corrupted file into the folder, **the system may crash**.  
- Advanced plugins (like **VolumeHeatMap** and **CVD**) are distributed separately and not included in this open-source repo.  

---

## 🎉 That’s it!

You are now ready to:

* Explore charts
* Analyze crypto markets
* Experiment with indicators

For developer details, see [Project Structure](./project-structure.md)