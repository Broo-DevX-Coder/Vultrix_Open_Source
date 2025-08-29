import logging
from PySide2.QtWidgets import QMenu, QAction
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QUrl
import os

from Data import ASSETS_HTML

BASE_ASSETS = ["USDT", "FDUSD", "USDC", "BUSD", "TUSD", "DAI"]
BASE_DIR = os.path.dirname(__file__)

class Wallet(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        logging.info("Wallet Page loaded and started")

        self.setUrl(QUrl(f'file:///{os.path.join(ASSETS_HTML,"wallet.html")}'))

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


    # ==== Click-right-list =====
    def show_context_menu(self, pos):
        menu = QMenu(self)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.back)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.forward)

        menu.addAction(back_action)
        menu.addAction(forward_action)
        menu.addSeparator()
        menu.addAction(reload_action)

        menu.exec_(self.mapToGlobal(pos))

    def update_bilances(self,total=0.0,avilable=0.0,frozen=0.0):
        self.page().runJavaScript(f"""
            document.getElementById('total-balance__main-card').innerHTML = "{total}";
            document.getElementById('avilabel-balance__main-card').innerHTML = "{avilable}";
            document.getElementById('frozen-balance__main-card').innerHTML = "{frozen}";
        """)

    def update_wallet(self,balances):
        list_html = ''
        for asset in balances:
            asset_name:str = asset["asset"]
            available = float(asset["free"])
            frozen = float(asset["locked"])
            if available + frozen == 0: continue
            pair_html = f""" <div class="pair" style="margin-top:5px;margin-bottom:5px;">
                    <div class="left">
                        <img src="https://api.elbstream.com/logos/crypto/{asset_name.lower()}" alt="{asset_name.upper()}" class="icon">
                        <span class="symbol">&nbsp;{asset_name.upper()}</span>
                    </div>
                    <div class="middle">
                        <span class="price">{round(available + frozen,2) if asset_name.upper() in BASE_ASSETS else available + frozen} {asset_name.upper()}</span>
                    </div>
                    <div class="balances">
                        <span class="available">{available}</span>
                        <span class="frozen">{frozen}</span>
                    </div>
                </div> 
            """
            list_html += pair_html
        self.page().runJavaScript(f""" document.getElementById('pairs-list__wallet').innerHTML = `{list_html}` """)

    # ======== Infrastructure defs ==============
    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            i.cancel()
        event.accept()
    # Start all functions and show window
    def run(self):
        self.show()