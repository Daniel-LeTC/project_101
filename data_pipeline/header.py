from time import perf_counter, sleep
from seleniumwire import webdriver
from login import login
import requests
import json
import pandas as pd
from driver import Driver

driver = Driver.get_driver()

def headers_get(url):
    global driver
    driver.get(url)
    driver.get_cookies()
    for request in driver.requests:
        pass
    print(request.headers)
    return request.headers


def get_cookies():
    return headers_get("https://en.52wmb.com/async/raw/trade/list?country=vietnam&ie=0&start_date=2023-04-06&end_date=2023-04-07&hs=54&des=&seller=&buyer=&seller_country=&seller_port=&buyer_port=&trans=&qty_min=&qty_max=&amount_min=&amount_max=&uusd_min=&uusd_max=&tag_id=&start=40")

