import os

from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtCore import Qt, QUrl
import logging

from Data import ASSETS_HTML

BASE_DIR = os.path.dirname(__file__)
QtWebEngine.initialize()

class Home(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        self.windows = []
        logging.info("Home Page loaded and started")

        self.setUrl(QUrl(f'file:///{os.path.join(ASSETS_HTML,"home.html")}'))

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

    def update_user_info(self,name,uid,type_):
        self.page().runJavaScript(f"""
            document.getElementById('user-name').innerHTML = "{name}";
            document.getElementById('user-binance-uid').innerHTML = "{uid}";
            document.getElementById('user-accont-type').innerHTML = "{type_}";
        """)


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