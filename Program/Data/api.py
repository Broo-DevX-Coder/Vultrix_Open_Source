import httpx
import time
import hmac
import hashlib
import logging
from . import logs

URL = "https://api.binance.com"

def create_signature(params, secret):
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature
        
def get_account_info(api_key:str,api_secret:str,session:httpx.Client=None):
    endpoint = "/api/v3/account"
    url = URL + endpoint
    params = {
        "timestamp": int(time.time() * 1000)
    }
    params["signature"] = create_signature(params, api_secret)
    headers = {"X-MBX-APIKEY": api_key}
    if session == None:
        response = httpx.get(url, headers=headers, params=params)
    else:
        response = session.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        r = response.json()
        if str(r) == "{}" or not r.get("code"):
            return True,r
    elif response.status_code == 400:
        logging.error(f"[Binance Privite API / Get Accont Info] -> This secreat key is unacceptable with api-key")
        return False,"SECREAT_KEY_ERROR"
    elif response.status_code == 401:
        logging.error(f"[Binance Privite API / Get Accont Info] -> invalide api-key or needed permetions")
        return False,"INVALID_API_KEY"
    else:
        logging.error(f"[Binance Privite API / Get Accont Info] -> Server Return Error Code: {response.status_code}")
        return False,"UNKNON_ERROR"

def get_prices(session:httpx.Client=None):
    url = URL + "/api/v3/ticker/price"
    if session != None: response = session.get(url)
    else: response = httpx.get(url)
    if response.status_code == 200:
        r = response.json()
        if isinstance(r,list):
            return {x["symbol"]: float(x["price"]) for x in r}
        else:
            logging.error(f"[Binance Public API / Get Prices] -> Server Return Error Message: {response.status_code}")
            return False
    else:
        logging.error(f"[Binance API / Get Prices] -> Server Return Error Code: {response.status_code}")
        return False
    

def get_total_balance_in_usdt(api_key,api_secreat,session:httpx.Client=None):

    accont = get_account_info(api_key,api_secreat,session)
    if accont[0] == True:balances = accont[1].get("balances")
    else:return False

    prices = get_prices(session)
    if prices == False: return False

    total_usdt = 0.0
    free_amount = 0.0
    locked_amount = 0.0

    for b in balances:
        asset = b["asset"]
        free = float(b["free"])
        locked = float(b["locked"])
        amount = free + locked
        if amount == 0:
            continue
        if asset == "USDT":
            total_usdt += amount
            free_amount += free
            locked_amount += locked
        else:
            symbol = asset + "USDT"
            if symbol in prices:
                total_usdt += amount * prices[symbol]
                free_amount += free * prices[symbol]
                locked_amount += locked * prices[symbol]
            else:
                # if no direct USDT pair, you could try BTC/USDT as a bridge
                pass
    
    return total_usdt,free_amount,locked_amount,balances