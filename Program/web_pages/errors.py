from .pup_messages import pup_message
from Data import logs
import logging


def error_429(x):
    logging.error(f"{x} -> ⚠️ Too many requests (429). Please wait just 1 minute to retry\nif you dont wait, you IP ADress will blocked")
    pup_message("Too many requests","⚠️ Too many requests (429). Please wait just 1 minute to retry\nif you dont wait, you IP Adress will blocked",None,"error")

def error_418(x):
    logging.error(f"{x} ->🚫 IP is banned temporarily (418)")
    pup_message("Too many requests","🚫 IP is banned temporarily (418). Please wait 1 hour to retry\nif you dont wait, you IP ADress will blocked",None,"error")

def error_403(x):
    logging.error(f"{x} ❌ Forbidden (403). Your IP might be blocked.")
    pup_message("Too many requests","❌ Forbidden (403). Your IP might be blocked. Please Try to use VPN or Proxy server",None,"error")

def connection_error(x):
    logging.critical(f"{x} ❌ No Internet Connection")
    pup_message("Too many requests","❌ No Internet Connection\nPlease Try to connect and retry",None,"error")

def unknown_error(x,d):
    logging.critical(f"{x} Unknown Error -> {d}")
    pup_message("Unknown Error","❌ Unknown error\nPlease TryAgain",None,"error")