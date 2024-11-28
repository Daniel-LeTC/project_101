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
    for request in driver.requests:
        pass
    return request.headers



