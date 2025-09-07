import os
import sys
import json
import asyncio
from datetime import datetime
import logging

os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"

import aiohttp
import httpx
import pandas as pd
import numpy as np
import pyqtgraph as pg
import websockets

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QGraphicsRectItem,QLabel,QSpinBox,QComboBox,QPushButton,QListWidget

# ===== Utils =====
from .utils import (
    DATE, 
    TimeAxis, 
    to_milliseconds, 
    QSS_BINANCE_STYLE, 
    binance_charts_theme,
    GlobalCursor,
    CandalsChart
)
from .utils import TIME_FRAMES_INTERVALS,qt_color_names,MAINCHART_ITEMS
from web_pages import error_403,error_429,error_418,connection_error
import logging

# ===== Helpers =====
def time_ms():
    """Return current time in milliseconds."""
    return int(datetime.now().timestamp() * 1000)
colors = CandalsChart.set_candals_color()

binance_charts_theme()

def connection_error_(x):
    connection_error(f"[Candals Chart][{x}]")

class SimpleCandelsChart(pg.GraphicsLayoutWidget):
    """Simple candlestick chart with live Binance data and moving averages."""

    # ===== Class constants =====
    CANDELS_WIDTH_PERCENT: float = 0.7

    def __init__(self,time_frame: str = "5m",max_candals: int = 100,symbol: str = "BTCUSDT",moving_average: list = [[20, 30, 60], ["blue", "yellow", "#1A2A80"], True]):
        super().__init__()
        self.async_tasks = []
        self.setStyleSheet(QSS_BINANCE_STYLE)

        # repare vars
        self.CANDELS_FRAME = time_frame
        self.MAX_CANDLES = max_candals
        self.SYMBOL = symbol
        self.MOVING_AVERAGE = moving_average
        self.last_price = 100
        self.PRICE_DICIAMEL = 2
        logging.info(f"Trading chart started on symbol `{symbol}`")

        # Time frame in milliseconds and unit
        self.FRAME = to_milliseconds(self.CANDELS_FRAME)

        # Window setup
        self.resize(900, 560)
        self.setWindowTitle(f"{self.SYMBOL} Price")

        # Plot setup
        self.time_axix = TimeAxis(orientation="bottom")
        self.VB = pg.ViewBox()
        self.plot = self.addPlot(viewBox=self.VB, axisItems={"bottom": self.time_axix})
        self.plot.showGrid(x=True, y=True, alpha=0.12)

        # State
        self.styles = {}
        self.widgets = {"cursor": {}, "curves": {}}
        self.candle_items = []           # Closed candles: {x: [line, rect]}
        self.not_closed_candel = []      # Current candle: [line, rect]

        # Styles
        self.styles["bg"] = lambda x: QtGui.QColor(str(x))
        self.TOP_Z_VALYE = lambda x: x.setZValue(1000)

        # Cursor / overlay setup
        self.widgets["cursor"]["lambda"] = lambda angle=0, style=QtCore.Qt.DashLine, color=(255, 255, 255, 150), width=0.5: pg.InfiniteLine(
            angle=float(angle),
            pen=pg.mkPen(color=color, width=width, style=style),
            movable=False
        )
        self.widgets["cursor"]["vline"] = self.widgets["cursor"]["lambda"](angle=90)
        self.widgets["cursor"]["hline"] = self.widgets["cursor"]["lambda"]()
        self.widgets["cursor"]["price_line"] = self.widgets["cursor"]["lambda"](color="#FFFFFF")
        self.widgets["cursor"]["price_pos"] = pg.TextItem()
        self.widgets["cursor"]["label_pos"] = pg.TextItem()
        self.widgets["cursor"]["label_pos2"] = pg.TextItem()
        self.widgets["top_label"] = pg.TextItem()

        # Add cursor items to plot
        for itm in ("vline", "hline", "label_pos", "label_pos2", "price_line", "price_pos"):
            self.plot.addItem(self.widgets["cursor"][itm])
            self.TOP_Z_VALYE(self.widgets["cursor"][itm])

        self.plot.addItem(self.widgets["top_label"])
        self.TOP_Z_VALYE(self.widgets["top_label"])

        # Top label set pos
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: self.widgets["top_label"].setPos(self.VB.viewRect().left(), self.VB.viewRect().bottom()))
        timer.start(50)

        # Top label HTML formatter
        if self.MOVING_AVERAGE[2]:

            movings = ''
            for v,c in list(zip(self.MOVING_AVERAGE[0], self.MOVING_AVERAGE[1])):
                movings += f'<br><font color="{c}">Moving average:{v} candels</font>'

            self.widgets["top_label_html"] = lambda curent_p, color, time: self.widgets["top_label"].setHtml(
                f"Frame:{self.CANDELS_FRAME}<br><font color='{color}'>{time}<br>{curent_p}</font>"
                f"{movings}"
            )
        else:
            self.widgets["top_label_html"] = lambda curent_p, color, time: self.widgets["top_label"].setHtml(
                f"Frame:{self.CANDELS_FRAME}<br><font color='{color}'>{time}<br>{curent_p}</font>"
            )
        

        # Connect mouse event
        self.scene().sigMouseMoved.connect(self.mouse_moved)
        self.VB.sigResized.connect(self.update_labels_pos)
        self.VB.sigRangeChanged.connect(lambda _, __: self.update_labels_pos())

        # Moving averages setup
        if self.MOVING_AVERAGE[2]:
            self.widgets["moving_average"] = {}
            self.Moving_Averages = list(enumerate(zip(self.MOVING_AVERAGE[0], self.MOVING_AVERAGE[1])))
            for i, m in self.Moving_Averages:
                self.widgets["moving_average"][i] = {"curve":self.plot.plot(
                    [0], [0], width=0.5, pen=pg.mkPen(color=str(m[1]))
                    ), "x":[], "y":[], "closes":[]}

    # ===== Events =====
    def mouse_moved(self, pos):
        """Update cursor position and labels on mouse move."""
        if self.plot.sceneBoundingRect().contains(pos):
            vb = self.plot.getViewBox()
            mousePoint = vb.mapSceneToView(pos)
            x_, y_ = mousePoint.x(), mousePoint.y()

            self.widgets["cursor"]["vline"].setPos(x_)
            self.widgets["cursor"]["hline"].setPos(y_)

            self.widgets["cursor"]["label_pos"].setPos(x_, y_)
            self.widgets["cursor"]["label_pos2"].setY(y_)

            try:
                dstr = DATE(x_)
            except Exception:
                dstr = ""

            GlobalCursor.set_label_pos(self.widgets["cursor"]["label_pos"],date_str=dstr,value_n="Price",value_v=y_,value_diciamles=self.PRICE_DICIAMEL)
            GlobalCursor.set_label_pos2(self.widgets["cursor"]["label_pos2"],y_,self.PRICE_DICIAMEL)
            
            self.widgets["cursor"]["price_pos"].setY(self.last_price)

            self.scene().update()

    def update_labels_pos(self):
            self.widgets["top_label"].setPos(self.VB.viewRect().left(), self.VB.viewRect().bottom())
            self.widgets["cursor"]["label_pos2"].setX(self.VB.viewRect().left())
            self.widgets["cursor"]["price_pos"].setX(self.VB.viewRect().left())


    # ===== Helpers =====
    def _draw_candle(self, x, o, h, l, c, w):
        """Draw a single candlestick (line + rectangle)."""
        top = max(o, c)
        bottom = min(o, c)
        height = top - bottom if top != bottom else 1e-8
        color = colors["candle_up"] if c >= o else colors["candle_down"]

        line = self.plot.plot([x, x], [l, h], pen=pg.mkPen(color))
        rect = QGraphicsRectItem(x - w / 2, bottom, w, height)
        rect.setPen(pg.mkPen(color))
        rect.setBrush(pg.mkBrush(color))
        self.plot.addItem(rect)

        return line, rect, color

    async def _load_initial(self):
        """Load initial candle data from Binance REST API with error handling."""
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": self.SYMBOL.upper(),"interval": self.FRAME[1],"limit": self.MAX_CANDLES}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(url, params=params)
                if r.status_code == 429:self.close(); return error_429("[Candals Chart][Binance REST]")
                if r.status_code == 418:self.close(); return error_418("[Candals Chart][Binance REST]")
                if r.status_code == 403:self.close(); return error_403("[Candals Chart][Binance REST]")
                r.raise_for_status()
                self.kligns = r.json()
        except httpx.ConnectError:
            self.close()
            return connection_error_("Binance REST")
        except Exception as e:
            self.close()
            logging.error(f"[Candals Chart][Binance REST] -> Unexpected error: {e}")
            return

        self.df = pd.DataFrame(self.kligns,columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        for col in ["open_time", "close_time", "open", "high", "low", "close","volume", "quote_asset_volume", "taker_buy_base_asset_volume","taker_buy_quote_asset_volume"]:
            self.df[col] = self.df[col].astype(float)

    async def _draw_candels(self, i, row, w):
        """Draw a single candle from DataFrame row."""
        x = float(row.open_time)
        o, h, l, c = float(row.open), float(row.high), float(row.low), float(row.close)

        line, rect, color = self._draw_candle(x, o, h, l, c, w)

        if i == self.MAX_CANDLES - 1 and (time_ms() < row.close_time):
            self.not_closed_candel.extend([line, rect])
        else:
            self.candle_items.append({str(x): [line, rect]})

        self.widgets["cursor"]["price_line"].setPos(c)
        self.widgets["cursor"]["price_pos"].setPos(self.VB.viewRect().left(), c)
        self.widgets["top_label"].setPos(self.VB.viewRect().left(), self.VB.viewRect().bottom())
        CandalsChart.set_price_label(self.widgets["cursor"]["price_pos"],price=c,up= c>=o, price_diciamles=self.PRICE_DICIAMEL)
        self.widgets["top_label_html"](str(c), "green" if c >= o else "red", DATE(x))

        self.last_price = c

    async def _draw_initial(self):
        """Draw all initial candles and moving averages."""
        w = self.FRAME[0] * self.CANDELS_WIDTH_PERCENT

        for i, row in enumerate(self.df.itertuples()):
            asyncio.create_task(self._draw_candels(i, row, w))

        if self.MOVING_AVERAGE[2]:
            for i, m in self.Moving_Averages:
                ma_values = self.df["close"].rolling(window=m[0]).mean()
                self.df["moving_average"] = ma_values

                self.widgets["moving_average"][i]["x"].extend(self.df.loc[ma_values.notnull(), "open_time"].to_list())
                self.widgets["moving_average"][i]["y"].extend(ma_values.dropna().to_list())
                self.widgets["moving_average"][i]["closes"].extend(self.df["close"].to_list())

                self.widgets["moving_average"][i]["curve"].setData(
                    self.widgets["moving_average"][i]["x"],
                    self.widgets["moving_average"][i]["y"]
                )

        last_open_time = float(self.df.iloc[-1]["open_time"]) if len(self.df) else 0
        self.plot.setXRange(last_open_time - 50 * self.FRAME[0], last_open_time + 20 * self.FRAME[0])
        self.plot.setYRange(float(self.df["low"].min()), float(self.df["high"].max()))
        self.VB.setLimits(xMin=float(self.df.iloc[0]["open_time"]))

    async def _draw_updated_candel(self, message):
        """Draw updated candle from live WebSocket data."""
        for itm in self.not_closed_candel:
            self.plot.removeItem(itm)
        self.not_closed_candel.clear()

        k = message["k"]
        x, o, h, l, c = float(k["t"]), float(k["o"]), float(k["h"]), float(k["l"]), float(k["c"])
        closed = bool(k["x"])

        w = self.FRAME[0] * self.CANDELS_WIDTH_PERCENT
        line, rect, color = self._draw_candle(x, o, h, l, c, w)

        if not closed:
            self.not_closed_candel.extend([line, rect])
        else:
            self.candle_items.append({str(x): [line, rect]})
            if self.MOVING_AVERAGE[2]:
                for i, m in self.Moving_Averages:
                    ma_values = self.df["close"].rolling(window=m[0]).mean()
                    self.df["moving_average"] = ma_values

                    self.widgets["moving_average"][i]["x"].append(x)
                    self.widgets["moving_average"][i]["closes"].append(c)
                    self.widgets["moving_average"][i]["y"].append(np.mean(self.widgets["moving_average"][i]["closes"][-m[0]:]))

                    self.widgets["moving_average"][i]["curve"].setData(
                        self.widgets["moving_average"][i]["x"],
                        self.widgets["moving_average"][i]["y"]
                    )

        self.widgets["cursor"]["price_line"].setPos(c)
        self.widgets["cursor"]["price_pos"].setPos(self.VB.viewRect().left(), c)
        self.widgets["top_label"].setPos(self.VB.viewRect().left(), self.VB.viewRect().bottom())
        CandalsChart.set_price_label(self.widgets["cursor"]["price_pos"],price=c,up= c>=o, price_diciamles=self.PRICE_DICIAMEL)
        self.widgets["top_label_html"](str(c), "green" if c >= o else "red", DATE(x))

        self.last_price = c

        if len(self.candle_items) > self.MAX_CANDLES:
            deleted = len(self.candle_items) - self.MAX_CANDLES
            for d in self.candle_items[0:deleted]:
                for t in d:
                    self.VB.setLimits(xMin=float(t))
                    for litem in d.get(str(t)):
                        self.plot.removeItem(litem)
            del self.candle_items[0:deleted]
            self.df.drop(index=self.df.index[0:deleted], inplace=True)

    async def update_price(self):
        """Listen for live price updates via WebSocket with error handling."""
        url = f"wss://stream.binance.com:9443/ws/{self.SYMBOL.lower()}@kline_{self.FRAME[1]}"
        try:
            async with websockets.connect(url) as ws:
                async for payload in ws:
                    message = json.loads(payload)
                    asyncio.create_task(self._draw_updated_candel(message))
                    self.scene().update()
        except websockets.exceptions.ConnectionClosedError:
            self.close()
            connection_error_("Binance WebSocket")
        except Exception as e:
            self.close()
            logging.error(f"[Candals Chart][Binance WebSocket] -> {e}")
            connection_error_("Binance WebSocket")

    async def _set_price_diciamel(self):
        url = "https://api.binance.com/api/v3/exchangeInfo"
        params = {"symbol": self.SYMBOL.upper()}
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(url, params=params) as r:
                    if r.status == 429:self.close(); return error_429("[Candals Chart][Binance Info]")
                    if r.status == 418:self.close(); return error_418("[Candals Chart][Binance Info]")
                    if r.status == 403:self.close(); return error_403("[Candals Chart][Binance Info]")
                    data = await r.json()
                    self.tick_size = float(data["symbols"][0]["filters"][0]["tickSize"])
                    self.PRICE_GROUPS_STEP: float = self.tick_size * 100
                    tick_str = f"{self.tick_size:.10f}".rstrip("0")
                    if '.' in tick_str:self.PRICE_DICIAMEL = len(tick_str.split(".")[1])
                    else: self.PRICE_DICIAMEL = 0
                    if "BTC" in str(data["symbols"][0]["symbol"]):
                        self.PRICE_GROUPS_STEP: float = self.tick_size * 1000
        except aiohttp.ClientConnectorError:
            self.close()
            connection_error_("Binance Info")
        except Exception as e:
            self.close()
            logging.error(f"[Candals Chart][Binance Info] ->Unexpected error: {e}")

    # ======== Infrastructure defs ==============

    # Reset ChowCharts When the olugin seted
    @staticmethod
    def reset_showchart_body(parent):
        parent.time_frame["label"].setText("Time frame")
        parent.setFixedSize(300, 533)
        parent.submit_button.setGeometry(5, 493, 290, 35)
        for i in ["combo_list","item_list","value_num","color_list","max_candals"]:
            parent.mainchart_items[i].show()
            parent.mainchart_items["labels"][i].show()
        parent.mainchart_items["add"].show()
        
        parent.mainchart_items["max_candals"].setGeometry(87, 150, 200, 35)
        parent.mainchart_items["combo_list"].setGeometry(87, 190, 200, 35)
        parent.mainchart_items["color_list"].setGeometry(87, 230, 200, 35)
        parent.mainchart_items["value_num"].setGeometry(87, 270, 200, 35)
        parent.mainchart_items["item_list"].setGeometry(5, 332, 290, 116)
        parent.mainchart_items["add"].setGeometry(5, 452, 290, 35)
        parent.mainchart_items["labels"]["max_candals"].move(10, 155)
        parent.mainchart_items["labels"]["combo_list"].move(10, 195)
        parent.mainchart_items["labels"]["color_list"].move(10, 235)
        parent.mainchart_items["labels"]["value_num"].move(10, 275)
        parent.mainchart_items["labels"]["item_list"].move(5, 312)
        parent.mainchart_items["is_correct"][0] = False if parent.mainchart_items["value_num"].value() in [None,0,'',""] else True
        parent.mainchart_items["is_correct"][1] = False if parent.mainchart_items["max_candals"].value() in [None,0,'',""] else True

        parent.time_frame["label_bottum"].setText("Binance candals intervals")
        parent.time_frame["main_list"].clear()
        parent.time_frame["main_list"].addItems(TIME_FRAMES_INTERVALS)
        parent.time_frame["main_list"].show()
        parent.time_frame['is_correct'] = True

    # Creat the shart wen Add Button in show shart pushed
    @staticmethod
    def submit_data(parent,chart):
        parent.time_frame_value = parent.time_frame["main_list"].currentText()
        max_candals = parent.mainchart_items["max_candals"].value()
        _are_mav = True if len(parent.mainchart_items["curves"]["moving_average"]) > 0 else False
        _mavs = [[],[],_are_mav]
        if _are_mav:
            for i in parent.mainchart_items["curves"]["moving_average"]:
               v,c = parent.mainchart_items["curves"]["moving_average"][i]
               _mavs[0].append(int(v))
               _mavs[1].append(c)
               
        w = chart(symbol=parent.symbol_value,time_frame=parent.time_frame_value,moving_average=_mavs,max_candals=max_candals)
        parent.windows.append(w)
        w.run()

    @staticmethod
    def set_chart_vars(parent):
        parent.mainchart_items_value = {}
        parent.mainchart_items = {"curves":{"moving_average":{}},"max_candals_correct":True}
        # Price Chart curves (moving_average)
        parent.mainchart_items["labels"] = {
                "combo_list":QLabel("Curve",parent),
                "value_num":QLabel("Curve Value",parent),
                "item_list":QLabel("Curve...",parent),
                "color_list":QLabel("Curve Color",parent),
                "max_candals":QLabel("Max Candals",parent)
            }
        parent.mainchart_items["max_candals"] = QSpinBox(parent)
        parent.mainchart_items["combo_list"] = QComboBox(parent)
        parent.mainchart_items["color_list"] = QComboBox(parent)
        parent.mainchart_items["value_num"] = QSpinBox(parent)
        parent.mainchart_items["add"] = QPushButton("Add",parent)
        parent.mainchart_items["item_list"] = QListWidget(parent)

        for i in ["combo_list","item_list","value_num","color_list","max_candals"]:
            parent.mainchart_items[i].hide()
            parent.mainchart_items["labels"][i].hide()
        parent.mainchart_items["add"].hide()

        parent.mainchart_items["is_correct"] = [False,True]
        parent.mainchart_items["max_candals"].setRange(100,1000)
        for i,m in MAINCHART_ITEMS:
            parent.mainchart_items["combo_list"].addItem(i,m)

        parent.mainchart_items["color_list"].addItems(qt_color_names)
        SimpleCandelsChart._e_(parent)

        parent.mainchart_items["value_num"].valueChanged.connect(lambda _: SimpleCandelsChart.on_write_main_chart_item_value(parent,text=_))
        parent.mainchart_items["max_candals"].valueChanged.connect(lambda _: SimpleCandelsChart.on_write_main_chart_max_candals(parent,text=_))
        parent.mainchart_items["add"].clicked.connect(lambda : SimpleCandelsChart.on_ad_curve(parent))
        parent.mainchart_items["item_list"].itemDoubleClicked.connect(lambda _: SimpleCandelsChart.remove_curve(parent,item=_))

    @staticmethod
    def _e_(parent):
        for i in parent.mainchart_items["is_correct"]: 
            if i == False: 
                parent.mainchart_items["add"].setEnabled(False)
                return
        parent.mainchart_items["add"].setEnabled(True)

    @staticmethod
    def _ee_(parent):
        if parent.symbol_input['is_correct'] == False or parent.shart_sellect['is_correct'] == False or parent.time_frame['is_correct'] == False or parent.mainchart_items["max_candals_correct"] == False:
            parent._e_(False)
        else:
            parent._e_(True)
        

    # On write main_chart_item value
    @staticmethod
    def on_write_main_chart_item_value(parent,text):
        if text not in [None,0,'',""]:
            parent.time_frame_value = int(text)
            parent.mainchart_items["is_correct"][0] = True
        else:
            parent.mainchart_items["is_correct"][0] = False
        SimpleCandelsChart._e_(parent)
            
    # On write main_chart_item value
    @staticmethod
    def on_write_main_chart_max_candals(parent,text):
        if text not in [None,0,'',""]:
            parent.time_frame_value = int(text)
            parent.mainchart_items["is_correct"][1] = True
        else:
            parent.mainchart_items["is_correct"][1] = False
        SimpleCandelsChart._ee_(parent)

    # On Push add curve in main_chart button 
    @staticmethod
    def on_ad_curve(parent):
        curve = parent.mainchart_items["combo_list"].itemData(parent.mainchart_items["combo_list"].currentIndex())
        color = parent.mainchart_items["color_list"].currentText()
        value = parent.mainchart_items["value_num"].value()

        parent.mainchart_items["curves"][curve][f"{curve} {value} {color}"] = [value,color]
        parent.mainchart_items["item_list"].addItem(f"{curve} {value} {color}")

        parent.mainchart_items["item_list"].update()

    @staticmethod
    def remove_curve(parent, item):
        # Get the text of the item (the key you stored: "curve:value:color")
        item_text = item.text()

        # Split to get curve name, value, color
        try:
            curve_name, value, color = item_text.split(" ")
            value = int(value)
        except ValueError:
            # fallback if format is unexpected
            curve_name = item_text
            value = None
            color = None

        # Remove from your internal dictionary if exists
        if curve_name in parent.mainchart_items["curves"]:
            key_to_remove = f"{curve_name} {value} {color}"
            del parent.mainchart_items["curves"][curve_name][key_to_remove]

        # Remove from the QListWidget
        row = parent.mainchart_items["item_list"].row(item)
        removed_item = parent.mainchart_items["item_list"].takeItem(row)
        del removed_item

    # ---------------------------------------------
    
    # Start async defs
    async def run_(self):
        """Run the chart: load data, draw, and update in real-time."""
        await self._load_initial()
        await self._draw_initial()
    
    # On close chart
    def closeEvent(self, event):
        for i in self.async_tasks:
            try:
                i.cancel()
            except:
                pass

        event.accept()

    # Start chart
    def run(self):
        task1 = asyncio.create_task(self.run_());task1
        task2 = asyncio.create_task(self._set_price_diciamel());task2
        self.show()
        task3 = asyncio.create_task(self.update_price());task3
        self.async_tasks.extend([task1,task2,task3])