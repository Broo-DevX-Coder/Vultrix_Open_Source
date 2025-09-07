import json
import logging
import os

import httpx
import websockets

# To force the program to use PySide2
os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"

import time
import asyncio
import pandas as pd
import pyqtgraph as pg

import aiohttp
from socket import gaierror
import qasync
import asyncio

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *

from .utils import *

class OrderBookSideWindow(QWidget):
    """Single-side Order Book (Bids or Asks) like Binance"""
    closed = QtCore.Signal(object)

    def __init__(self, symbol: str, price_decimals: int, vol_unit: str, side: str):
        super().__init__()
        self.setWindowTitle(f"{symbol} Order Book - {side.capitalize()}")
        self.resize(400, 600)
        self.setFixedWidth(400)
        self.setStyleSheet(QSS_BINANCE_STYLE)

        self.symbol = symbol
        self.PRICE_DECIMALS = price_decimals
        self.VOL_UNIT = vol_unit
        self.side = side  # "bids" or "asks"

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Price", f"Quantity ({vol_unit})", "Quantity (USD)"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget { background-color: black; color: white; gridline-color: #333; }
            QHeaderView::section { background-color: #111; color: #ccc; }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def update_side(self, levels: list):
        """
        Update the table with one side of the order book.
        levels: list of (price, qty)
        """
        self.table.setRowCount(len(levels))

        if self.side == "asks":
            # asks => sorted ascending (lowest ask on top)
            levels = sorted(levels, key=lambda x: x[0])
            color = "red"
        else:
            # bids => sorted descending (highest bid on top)
            levels = sorted(levels, key=lambda x: -x[0])
            color = "lime"

        for i, (p, q) in enumerate(levels):
            self._set_row(i, p, q, p*q, color=color)

    def _set_row(self, row, price, qty, cum, color="white"):
        """Helper to insert one row into table"""
        price_item = QTableWidgetItem(f"{price:.{self.PRICE_DECIMALS}f}")
        qty_item = QTableWidgetItem(f"{qty:.4f}")
        total_item = QTableWidgetItem(f"{cum:.4f}")

        for item in (price_item, qty_item, total_item):
            item.setTextAlignment(QtCore.Qt.AlignCenter)

        # color price cell
        price_item.setForeground(QtGui.QColor(color))

        self.table.setItem(row, 0, price_item)
        self.table.setItem(row, 1, qty_item)
        self.table.setItem(row, 2, total_item)

    def closeEvent(self, event):
        try:
            self.closed.emit(self)
        except Exception:
            pass
        super().closeEvent(event)

    def run(self):
        self.show()

class OrderBook():
    """Custom chart widget for visualizing Binance order book depth."""

    def __init__(self,**keyargs):
        self.async_tasks = []
        self.opened_windows = []
        logging.info(f"[Order Book] Start VolumeheatMap for `{keyargs['symbol']}`")

        # Set Vars
        self.TIME_MS: int = int(keyargs["time_frame"])*1000
        self.SYMBOL = keyargs["symbol"]
        self.SCATTER_SIZE = 10
        self.PRICE_DICIAMELS = 2
        self.PRICE_GROUPS_STEP = 1
        self.ORDERBOOK_LIMIT = 3000

        self.global_asks = {}
        self.global_bids = {}
        self.snapshot_update = 0
        self.snapshot_update_status = 0
        self.updates = {}
        self.bests_ob = {"min":{"asks":0,"bids":0},"max":{"asks":0,"bids":0}}

        self.rest_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(20))


    def time_n(self):
        """Return current time in milliseconds."""
        return time.time() * 1000

    async def _update(self):
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": self.SYMBOL.upper(),"limit": self.ORDERBOOK_LIMIT}
        self.snapshot_update_status = 0
        try:

            await asyncio.sleep(1)
            
            async with self.rest_session.get(url, params=params) as r:
            
                if r.status == 429:self.close();return error_429("[Order Book][Binance Depth API]")
                if r.status == 418:self.close();return error_418("[Order Book][Binance Depth API]")
                if r.status == 403:self.close();return error_403("[Order Book][Binance Depth API]")
                if r.status != 200:
                    self.close()
                    unknown_error("[Order Book][Binance Depth API]",f"Unexpected HTTP {r.status}")
                depth_dict = await r.json()
                self.snapshot_update = depth_dict.get("lastUpdateId")
                self.snapshot_update_status = 10

                self.global_asks = {float(p):float(q) for p,q in depth_dict.get("asks")}
                self.global_bids = {float(p):float(q) for p,q in depth_dict.get("bids")}
                self.bests_ob = {
                    "min":{
                        "asks":min(self.global_asks.keys()),
                        "bids":min(self.global_bids.keys())
                    },
                    "max":{
                        "asks":max(self.global_asks.keys()),
                        "bids":max(self.global_bids.keys())
                    }}
                logging.info("[Order Book][Binance Depth API] Get ordrbook Snapshot")

                for win in self.opened_windows:
                    win.bests_ob = self.bests_ob

        except (aiohttp.ClientConnectionError,gaierror):
            self.close()
            return connection_error("[Order Book][Binance Depth API]")
        except Exception as e:
            self.close()
            return unknown_error("[Order Book][Binance Depth API]",f"Unexpected polling error: {e}")
        

    async def _polling_update(self):
        start_time__ = self.time_n()
        uri = f"wss://stream.binance.com:9443/stream?streams={self.SYMBOL.lower()}@depth@100ms"
        try:
            async with websockets.connect(uri) as ws:
                logging.info("[Order Book][Binance websoket] Start websoket")
                last = 0
                asyncio.create_task(self._update())
                while True:
                    msg = json.loads(await ws.recv()).get("data")
                    lastUpdateId = msg.get("u")
                    firstUpdateId = msg.get("U")

                    if self.snapshot_update_status == 0: 
                        self.updates[lastUpdateId] = msg

                    elif self.snapshot_update_status == -1:
                        if not last+1 == firstUpdateId:
                            asyncio.create_task(self._update())
                            continue

                        asks_ = msg.get("a")
                        bids_ = msg.get("b")

                        self._update_ob(asks_,bids_)
                        last = lastUpdateId

                    else:
                        last_updates_key = list(self.updates.keys())[-1] if len(list(self.updates.keys())) > 0 else lastUpdateId
                        self.snapshot_update_status = -1

                        if last_updates_key == self.snapshot_update:
                            asks_ = msg.get("a")
                            bids_ = msg.get("b")

                            self._update_ob(asks_,bids_)
                            last = lastUpdateId

                        else:
                            udpdates_keys = list(self.updates.keys())

                            if self.snapshot_update in udpdates_keys:
                                idx = udpdates_keys.index(self.snapshot_update)
                                vals = {k:self.updates[k] for k in udpdates_keys[idx:]}

                                for last,value in vals.items():
                                    vals_asks = value.get("a")
                                    vals_bids = value.get("b")
                                    self._update_ob(vals_asks,vals_bids)
                                    self.updates.clear()

                                asks_ = msg.get("a")
                                bids_ = msg.get("b")

                                self._update_ob(asks_,bids_)
                                last = lastUpdateId
                            else:
                                asyncio.create_task(self._update())
                                continue

                    if self.snapshot_update_status == -1 and self.time_n() >= start_time__+self.TIME_MS and len(self.opened_windows) != 0:
                        b_ = self.global_bids.items()
                        a_ = self.global_asks.items()

                        for win in self.opened_windows:
                            if win.side == "bids": win.update_side(list(self.global_bids.items()))
                            if win.side ==  "asks": win.update_side(list(self.global_asks.items()))
                            

                        start_time__ = self.time_n()
            
        except (websockets.exceptions.ConnectionClosedError,gaierror):
            self.close()
            connection_error("[Order Book][Binance websoket]")
        except Exception as e:
            self.close()
            return unknown_error("[Order Book][Binance websoket]",f"Unexpected error: {e}")

    def _update_ob(self,asks_,bids_):
        for p,q in bids_:
            q = float(q)
            p = float(p)
            self.global_bids[p] = q
            if self.global_bids[p] == 0: 
                del self.global_bids[p]
        for p,q in asks_:
            q = float(q)
            p = float(p)
            self.global_asks[p] = q
            if self.global_asks[p] == 0: 
                del self.global_asks[p]

    async def _set_price_groups_step(self):
        url = "https://api.binance.com/api/v3/exchangeInfo"
        params = {"symbol": self.SYMBOL.upper()}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                    r = await client.get(url, params=params)

                    if r.status_code == 429:self.close();return error_429("[Order Book][Binance ExchangeInfo API]")
                    if r.status_code == 418:self.close();return error_418("[Order Book][Binance ExchangeInfo API]")
                    if r.status_code == 403:self.close();return error_403("[Order Book][Binance ExchangeInfo API]")

                    if r.status_code != 200:
                        self.close()
                        return unknown_error("[Order Book][Binance ExchangeInfo API]",f"Unexpected HTTP {r.status}")

                    data = r.json()
                    self.tick_size = float(data["symbols"][0]["filters"][0]["tickSize"])
                    self.PRICE_GROUPS_STEP: float = self.tick_size * 100
                    tick_str = f"{self.tick_size:.10f}".rstrip("0")

                    if '.' in tick_str:self.PRICE_DICIAMELS = len(tick_str.split(".")[1])
                    else: self.PRICE_DICIAMELS = 0

                    if "BTC" in str(data["symbols"][0]["symbol"]):
                        self.PRICE_GROUPS_STEP: float = self.tick_size * 1000
        except (httpx.ConnectError,gaierror):
            self.close()
            return connection_error("[Order Book][Binance ExchangeInfo API]")
        except Exception as e:
            self.close()
            return unknown_error("[Order Book][Binance ExchangeInfo API]",f"ExchangeInfo error: {e}")

    # ======== Infrastructure defs ==============

    # Reset ChowCharts When the olugin seted
    @staticmethod
    def reset_showchart_body(parent):
        parent.setFixedSize(300, 185)
        parent.time_frame["label"].setText("Time delta")
        parent.submit_button.setGeometry(5, 145, 290, 35)
        for i in ["combo_list","item_list","value_num","color_list","max_candals"]:
            parent.mainchart_items[i].hide()
            parent.mainchart_items["labels"][i].hide()
        parent.mainchart_items["add"].hide()
        
        parent.time_frame["main_num"].show()
        parent.time_frame["label_bottum"].setText("Secondes unit")
        parent.time_frame['is_correct'] = False if parent.time_frame["main_num"].value() in [None,0,'',""] else True

    # Creat the shart wen Add Button in show shart pushed
    @staticmethod
    def submit_data(parent,chart):
        parent.time_frame_value = parent.time_frame["main_num"].value()
        w = chart(symbol=parent.symbol_value,time_frame=parent.time_frame_value)
        parent.windows.append(w)
        w.run()

    @staticmethod
    def set_chart_vars(parent):
        pass

    # ======================================================

    def close(self):
        # Non-blocking request to close async resources
        try:
            asyncio.create_task(self.close_async())
            for win in self.opened_windows:
                win.close()
        except (RuntimeError,RuntimeWarning):
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.close_async())
            except Exception:
                pass

    async def colse_session(self):
        await self.rest_session.close()

    def _on_child_closed(self, win):
        """Called when a child OrderBookSideWindow is closed."""
        try:
            if win in self.opened_windows:
                self.opened_windows.remove(win)
        except Exception:
            pass

        if len(self.opened_windows) == 0:
            # schedule the async close (don't await here)
            try:
                asyncio.create_task(self.close_async())
            except Exception:
                # fallback to call close() which schedules close_async
                self.close()

    async def close_async(self):
        """Proper async shutdown: close rest session, cancel tasks, close windows."""
        # prevent re-entrance
        if getattr(self, "_closing", False):
            return
        self._closing = True

        # cancel background tasks gracefully
        for t in list(self.async_tasks):
            try:
                t.cancel()
            except Exception:
                pass

        # allow tasks to cancel
        await asyncio.sleep(0)

        # close rest session
        try:
            await self.rest_session.close()
        except Exception:
            pass

        # close any remaining windows (safe)
        for win in list(self.opened_windows):
            try:
                win.close()
            except Exception:
                pass
        self.opened_windows.clear()

        logging.info(f"Order Book for {self.SYMBOL.upper()} Closed")


    # Start chart
    def run(self):
        """Run background update tasks."""
        bids_win = OrderBookSideWindow(self.SYMBOL.upper(), 2, self.SYMBOL.upper().replace("USDT",""), side="bids")
        asks_win = OrderBookSideWindow(self.SYMBOL.upper(), 2, self.SYMBOL.upper().replace("USDT",""), side="asks")
        
        for win in (asks_win, bids_win):
            win.closed.connect(self._on_child_closed)
            self.opened_windows.append(win)

        task1 = asyncio.create_task(self._set_price_groups_step());task1
        task3 = asyncio.create_task(self._polling_update());task3
        self.async_tasks.extend([task1,task3])

        for win in self.opened_windows:
            try:win.run()
            except Exception: pass