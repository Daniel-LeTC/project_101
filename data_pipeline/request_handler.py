from http.client import responses

import  requests
from time import perf_counter, sleep
from bs4 import BeautifulSoup
from header import headers_get, get_cookies, driver

request_time_interval = 0
class RequestHandler:
    def __init__(self, timeout=10, retries=3):
        self.header = get_cookies()
        self.timeout = timeout
        self.retries = retries
        self.isSuccess = False
        self.is_getting_header = False
        self.max_attempts = 5

    def handle_fetch_failed(self,url):
        print("Lấy header cho: ",url)
        self.is_getting_header = True
        if perf_counter() - request_time_interval < 6:
            sleep(perf_counter() - request_time_interval)
        self.header =headers_get(url)
        self.is_getting_header = False