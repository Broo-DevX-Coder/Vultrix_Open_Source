import asyncio
import logging
import sys
import os
from functools import partial

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import httpx

from Styles import MAIN_W_TOOL_BAR
from .show_sharts import ChowSharts

BASE_DIR = os.path.dirname(__file__)

from .utils import MW_STACKED_WINDOWS,MW_WINDOW_STAKED_BUTTONS,MW_POPUP_WIDOWS_BUTTONS,MW_POPUP_WIDOWS
from Data import get_total_balance_in_usdt,ASSETS_ICONS_SVG,ASSETS_ICONS_ICO
from Data.user_data import *

MW_POPUP_WIDOWS["Charts"] = {"m":ChowSharts,"ft?":True,"align":"rt"}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        size = [1100,800]
        self.setMinimumSize(size[0],size[1])
        self.async_tasks = []
        self.windows = []
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"main.ico")))
        logging.info("Show main-window")
        


        # ===== Windows system ==========
        # Stacked windows
        self.stack = QStackedWidget(self)
        self.stcked_windows = {}
        for u,i in MW_STACKED_WINDOWS.items(): 
            self.stcked_windows[u] = i()
        self.stcked_windows_layouts = {}
        
        # pop-up windows
        self.popup_windows = {}
        for u,i in MW_POPUP_WIDOWS.items(): 
            g = i
            g["m"] = i["m"](self)
            self.popup_windows[u] = g
            

        # ======= Create Toolbar =========
        self.tool_bar = {"w": QWidget(self),"geometry":[10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55],"stacks":{},"pop-up":{}}
        self.tool_bar["w"].setStyleSheet(MAIN_W_TOOL_BAR)

        tool_bar_layout = QHBoxLayout(self.tool_bar["w"])
        tool_bar_layout.setContentsMargins(0, 0, 0, 0)
        tool_bar_layout.setSpacing(25)
        tool_bar_layout.setAlignment(Qt.AlignCenter)

        # ----- tool Bar Items ----------
        # Normal windows
        windows_stackes_buttons = MW_WINDOW_STAKED_BUTTONS
        for icon,tooltip in windows_stackes_buttons.items():
            btn = QPushButton()
            btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
            btn.setIconSize(QSize(26, 26))
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            self.tool_bar["stacks"][f"btn_{icon}"] = btn
            self.tool_bar["stacks"][f"btn_{icon}"].clicked.connect(partial(self.cahnge_window,tooltip))
            tool_bar_layout.addWidget(btn)
        
        # Pop-Up windows (like the toolbar)
        pop_up_windows_buttons = MW_POPUP_WIDOWS_BUTTONS
        for icon,tooltip in pop_up_windows_buttons.items():
            btn = QPushButton()
            btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
            btn.setIconSize(QSize(26, 26))
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            self.tool_bar["pop-up"][f"btn_{icon}"] = btn
            self.tool_bar["pop-up"][f"btn_{icon}"].clicked.connect(partial(self.hide_show_popup_window,tooltip))
            tool_bar_layout.addWidget(btn)
        
        self.tool_bar["stacks"][f"btn_home"].setChecked(True)


        # ========== Windows =============
        # Staked
        for i,s in self.stcked_windows.items():
            self.stack.addWidget(s)
        self.setCentralWidget(self.stack)

        # Pop-Up
        for u,i in self.popup_windows.items():
            i["m"].hide()
            self.windows.append(i["m"])

        self.move_popup_windows()


    # ======== Slots ============
    # To Change main window
    def cahnge_window(self,w:str):
        self.stack.setCurrentWidget(self.stcked_windows.get(w))
        for i,t in self.tool_bar["stacks"].items():
            self.tool_bar["stacks"][i].setChecked(False)

        self.tool_bar["stacks"][f"btn_{w.lower()}"].setChecked(True)

    # Show-Run-Hide pupups windows
    def hide_show_popup_window(self,t:str):
        if self.popup_windows.get(t):
            checked = self.tool_bar["pop-up"][f"btn_{t.lower()}"].isChecked()
            if not checked:
                self.popup_windows[t]["m"].hide()
                self.tool_bar["pop-up"][f"btn_{t.lower()}"].setChecked(False)
            else:
                if self.popup_windows[t]["ft?"]:
                    self.popup_windows[t]["m"].run()
                    self.popup_windows[t]["ft?"] = False
                
                self.popup_windows[t]["m"].show()
                self.tool_bar["pop-up"][f"btn_{t.lower()}"].setChecked(True)

    # Move the Charts widget to the right place
    def move_popup_windows(self):
        for u,i in self.popup_windows.items():
            if i["align"] == "rt":
                i["m"].setGeometry(
                    self.width()-i["m"].width()-20,
                    20,
                    i["m"].width(),
                    i["m"].height()
                )
            elif i["align"] == "lt":
                i["m"].setGeometry(
                    20,
                    20,
                    i["m"].width(),
                    i["m"].height()
                )
            elif i["align"] == "rb":
                i["m"].setGeometry(
                    self.width()-i["m"].width()-20,
                    self.height()-i["m"].height()-20,
                    i["m"].width(),
                    i["m"].height()
                )
            elif i["align"] == "lb":
                i["m"].setGeometry(
                    20,
                    self.height()-i["m"].height()-20,
                    i["m"].width(),
                    i["m"].height()
                )

    # ============= pooling =================
    async def update_user_data_on_ui(self):
        await asyncio.sleep(5)
        self.stcked_windows["Home"].update_user_info(USER_NAME,USER_UID,USER_ATYPE)
        with httpx.Client(timeout=30) as session:
            while True:
                balances = get_total_balance_in_usdt(USER_API,USER_SECREAT,session)
                if balances != False:
                    total = round(float(balances[0]),2)
                    avilable = round(float(balances[1]),2)
                    frozen = round(float(balances[2]),2)
                    balances_wallet = balances[3]

                    self.stcked_windows["Home"].update_bilances(total,avilable,frozen)
                    self.stcked_windows["Wallet"].update_bilances(total,avilable,frozen)
                    self.stcked_windows["Wallet"].update_wallet(balances_wallet)
                else:
                    print("error")
                    await asyncio.sleep(5)
                    continue
                await asyncio.sleep(10)

    


    # ======== Infrastructure defs ==============

    # On extend window
    def resizeEvent(self, event):
        self.tool_bar["w"].setGeometry(self.tool_bar["geometry"][0],self.height() - 70,self.tool_bar["geometry"][2],self.tool_bar["geometry"][3])
        self.move_popup_windows()
        return super().resizeEvent(event)

    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            try:i.cancel()
            except:pass
        event.accept()
        logging.info("Parogram closed")
        sys.exit()

    def run(self):
        task1 = asyncio.create_task(self.update_user_data_on_ui());task1
        self.async_tasks.append(task1)
        self.show()
