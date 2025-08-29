from datetime import datetime
import logging
import os
import warnings
from .utils import APP_DATA

LOGS_FILE = os.path.join(APP_DATA,"logs/")
os.makedirs(LOGS_FILE,exist_ok=True)

# logging place ============================================================
logging.basicConfig(
    level=logging.INFO,               # Minimum level to log 
    handlers=[
        logging.FileHandler(filename=os.path.join(LOGS_FILE,str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".log"),mode="w"), # To Save evry thing in the log file
        logging.StreamHandler()
    ],                      
    format="%(asctime)s [%(levelname)s] -> %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",       # Date/time format
    style='%'                          # Format style (default is '%', can use '{')
)

logging.info("Logging is ready")

logging.getLogger("websockets").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("qasync").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

warnings.filterwarnings("ignore", message=".*Task was destroyed but it is pending!*")