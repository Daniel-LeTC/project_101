
import  requests
from time import perf_counter, sleep
from bs4 import BeautifulSoup
from header import headers_get, driver

request_time_interval = 0

class RequestHandler:
    def __init__(self, timeout=10, retries=3):
        self.headers = headers_get("https://en.52wmb.com/async/raw/trade/list?country=vietnam&ie=0&start_date=2023-04-06"
                                   "&end_date=2023-04-07&hs=54&des=&seller=&buyer=&seller_country=&seller_port=&"
                                   "buyer_port=&trans=&qty_min=&qty_max=&amount_min=&amount_max=&uusd_min=&uusd_max=&tag_id=&start=40")
        self.timeout = timeout
        self.retries = retries
        self.isSuccess = True

    def get_bill_id(self, url:str) -> requests.Response():
        attempt = 0
        for attempt in range(self.retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                temp_bill_id = soup.find_all("tr")
                if len(temp_bill_id) >= 1:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Lỗi khi fetch URL: {url}, Lần thử: {attempt + 1}, Error: {e}")
            finally:
                self.handle_fetch_failed(url)
        self.isSuccess = attempt == self.retries - 1

        return response


    def handle_fetch_failed(self,url):
        if perf_counter() -request_time_interval <6:
            sleep(perf_counter() - request_time_interval)
        return headers_get(url)

