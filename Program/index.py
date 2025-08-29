import asyncio
from core.open_program import OpenProgram
import qasync
from PySide2.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
loop = qasync.QEventLoop()

async def main():
    win = OpenProgram()
    win.show()
    while True:
        await asyncio.sleep(1)
try:
    with loop:
        loop.run_until_complete(main())
except (RuntimeError, KeyboardInterrupt):
    pass