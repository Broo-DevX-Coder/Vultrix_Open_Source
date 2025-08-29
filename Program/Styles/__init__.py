import os
from .binance_plot_them import binance_charts_theme,GlobalCursor,CandalsChart
from Data import ASSETS_QSS

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(ASSETS_QSS,"binance.qss"),"r") as f:
    QSS_BINANCE_STYLE = str(f.read())

with open(os.path.join(ASSETS_QSS,"main_w_tool_bar.qss"),"r") as f:
    MAIN_W_TOOL_BAR = str(f.read())

with open(os.path.join(ASSETS_QSS,"popup_w.qss"),"r") as f:
    POP_UP_WINDOW = str(f.read())
