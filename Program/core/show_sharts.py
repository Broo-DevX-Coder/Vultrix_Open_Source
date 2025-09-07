import os
import asyncio
import logging
import sys

os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu"

import httpx

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .utils import (
    CHARTS
)
from .shart_classes import CHARTS_CLASSES
from Styles import QSS_BINANCE_STYLE
from web_pages import error_403,error_429,error_418
from Data import ASSETS_ICONS_ICO

class ChowSharts(QWidget):
    clicked = Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.async_tasks = []
        self.spot_symbols = []

        # ===== Window Settings =====
        self.setWindowTitle("Chart Viewer")
        self.setFixedSize(300, 185)
        self.setStyleSheet(QSS_BINANCE_STYLE)
        self.setAttribute(Qt.WA_StyledBackground, True)
        logging.info("Show show-sahrts")
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"charts.ico")))

        # Values Vars
        self.symbol_value = ''
        self.chart_value = ''
        self.time_frame_value = ''

        # ===== Create Widgets =======
        self.symbol_input = {}
        self.shart_sellect = {}
        self.time_frame = {}
        self.windows = []

        # Set Enabled button
        self.symbol_input['is_correct'] = True
        self.shart_sellect['is_correct'] = True
        self.time_frame['is_correct'] = False

        # Set charts vars:
        for name,chart in CHARTS_CLASSES.items():
            try:chart.set_chart_vars(self)
            except:pass

        # Symbol input
        self.symbol_input["label"] = QLabel("Symbol", self)
        self.symbol_input["label"].move(10, 13)
        self.symbol_input["main"] = QComboBox(self)
        self.symbol_input["main"].setEditable(True)
        self.symbol_input["main"].setGeometry(87, 8, 200, 35)

        # Chart select
        self.shart_sellect["label"] = QLabel("Shart", self)
        self.shart_sellect["label"].move(10, 53)
        self.shart_sellect["main"] = QComboBox(self)
        self.shart_sellect["main"].setGeometry(87, 48, 200, 35)
        for t, i in CHARTS:
            self.shart_sellect["main"].addItem(t, i)

        # Submit button
        self.submit_button = QPushButton("Add Shart",self)
        self.submit_button.setGeometry(5, 145, 290, 35)

        # Time frame select
        self.time_frame["label"] = QLabel("Time frame", self)
        self.time_frame["label_bottum"] = QLabel("Binance candals intervals", self)
        self.time_frame["label"].move(10, 93)
        self.time_frame["label_bottum"].move(87, 125)

        self.time_frame["main_list"] = QComboBox(self)
        self.time_frame["main_list"].setGeometry(87, 88, 200, 35)
        self.time_frame["main_num"] = QSpinBox(self)
        self.time_frame["main_num"].setGeometry(87, 88, 200, 35)

        
        # set time frame
        self.chart_value = self.shart_sellect["main"].itemData(self.shart_sellect["main"].currentIndex())
        self.on_select_chart(self.shart_sellect["main"].currentIndex())

        # ======= set signals ========
        self.shart_sellect["main"].currentIndexChanged.connect(self.on_select_chart) # On select any shart
        self.symbol_input["main"].currentTextChanged.connect(self.on_write_symbol) # On write my symbol
        self.time_frame["main_num"].valueChanged.connect(self.on_wright_timefarme_secoundes)
        
        self.submit_button.clicked.connect(self.on_submit)
        

    # ============ Slots =================

    # On select Chart 
    def on_select_chart(self, index):
        data = self.shart_sellect["main"].itemData(index)
        self.chart_value = data
        self.time_frame["main_num"].hide()
        self.time_frame["main_list"].hide()
        CHARTS_CLASSES[data].reset_showchart_body(self)

    def _e_(self,d):
        self.submit_button.setEnabled(d)
    
    def _enable_(self):
        if self.symbol_input['is_correct'] == False or self.shart_sellect['is_correct'] == False or self.time_frame['is_correct'] == False:
            self._e_(False)
        else:
            self._e_(True)

    # On write time frame by secoundes
    def on_wright_timefarme_secoundes(self,text):
        if text not in [None,0,'',""]:
            self.time_frame_value = int(text)
            self.time_frame['is_correct'] = True
        else:
            self.time_frame['is_correct'] = False
        self._enable_()

    # On write symbol
    def on_write_symbol(self,symbol):
        if symbol in self.spot_symbols and len(self.spot_symbols) > 0:
            self.symbol_value = symbol
            self.symbol_input['is_correct'] = True
        else:
            self.symbol_input['is_correct'] = False
        self._enable_()

    # on push add shart button
    def on_submit(self):   
        CHARTS_CLASSES[self.chart_value].submit_data(self,CHARTS_CLASSES[self.chart_value])
    
     # ============ Authers =================
    def get_symbols(self):
        try:
            url = "https://api.binance.com/api/v3/exchangeInfo"
            response = httpx.get(url)
            data = response.json()
            if response.status_code == 200:
                self.spot_symbols = [
                    s['symbol'] 
                    for s in data['symbols'] 
                    if s['isSpotTradingAllowed'] and 
                    str(s['symbol']).endswith("USDT")
                ]
                # Add all Symbols:
                self.symbol_input["main"].addItems(self.spot_symbols)
            elif response.status_code == 429:
               error_429("[Show Charts][Get Symbols]")
            elif response.status_code == 418:
                error_418("[Show Charts][Get Symbols]")
            elif response.status_code == 403:
                error_403("[Show Charts][Get Symbols]")
            else:
                print("Unexpected error:", response.status_code, response.text)
        except Exception as e:
            logging.error(f"[Show Charts][Get Symbols] -> {e}")

        self.symbol_input['is_correct'] = True if len(self.spot_symbols) > 0 else False

    # ======== Infrastructure defs ==============

    # On click in widget
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            i.cancel()
        event.accept()
        logging.info("Parogram closed")
        sys.exit()

    def run(self):
        self.show()
        self.get_symbols()