from Styles import QSS_BINANCE_STYLE
from typing import Callable
from PySide2.QtWidgets import QMessageBox

def pup_message(
    title: str,
    text: str,
    function: Callable[[], None] | any,
    type_: str = "info"
):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)

    if type_ == "error":
        icon = QMessageBox.Critical
    elif type_ == "warning":
        icon = QMessageBox.Warning
    else:
        icon = QMessageBox.Information

    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setStyleSheet(QSS_BINANCE_STYLE)

    result = msg.exec_()  # use exec() if PyQt6/PySide6
    if result == QMessageBox.Ok:
        if isinstance(function,Callable):
            function()
