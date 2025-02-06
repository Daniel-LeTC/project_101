from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import sleep, perf_counter
from urllib.parse import quote

from bs4 import BeautifulSoup
from urllib import parse
import requests
import pandas as pd
import numpy as np

from util import Driver,headers_get, get_cookies

driver = Driver.get_driver()
lock = Lock()
class GetBillIDProcess:
    def __init__(self, total_bill, start_date, end_date, hscode,
                 transaction_type , buyer, supplier, description,
                 seller_country, seller_port, buyer_port, trans,
                 qty_min, qty_max, amount_min, amount_max,
                 uusd_min, uusd_max):

        self.start_date = start_date or ''
        self.end_date = end_date or start_date
        self.hscode = hscode or ''
        self.transaction_type = transaction_type or ''
        self.buyer = buyer or ''
        self.seller = supplier or ''
        self.description = description or ''
        self.seller_country = seller_country or ''
        self.seller_port = seller_port or ''
        self.buyer_port = buyer_port or ''
        self.trans = trans or ''
        self.qty_min = qty_min or ''
        self.qty_max = qty_max or ''
        self.amount_min = amount_min or ''
        self.amount_max = amount_max or ''
        self.uusd_min = uusd_min or ''
        self.uusd_max = uusd_max or ''
        self.total_bill = total_bill or ''
        self.pages_list = []
        self.final_page = (total_bill // 20) + 1
        self.expect_bill_of_final_page = self.total_bill % 20
        self.pages = range(0, self.final_page, 1)
        self.driver = Driver.get_driver()
        self.lock = Lock()
        self.start = 0
        self.trade_dates = []
        self.bill_ids = []
        self.bill_id_headers = []
        self.error_bill_ids = []
        self.isSuccessful = True
        self.header = None



    def generate_url(self, i):
        transaction_type_code = "1" if self.transaction_type == "export" else "0"

        # Khởi tạo URL với các tham số bắt buộc
        url = f"https://en.52wmb.com/async/raw/trade/list?country=vietnam&=undefined&ie={transaction_type_code}"

        # Thêm từng tham số động
        url += f"&start_date={self.start_date}&end_date={self.end_date}"
        url += f"&hs={self.hscode}"
        url += f"&des={parse.quote(self.description)}"
        url += f"&seller={parse.quote(self.seller)}"
        url += f"&buyer={parse.quote(self.buyer)}"
        url += f"&seller_country={parse.quote(self.seller_country)}"
        url += f"&seller_port={parse.quote(self.seller_port)}"
        url += f"&buyer_port={parse.quote(self.buyer_port)}"
        url += f"&trans={self.trans}" # transport
        url += f"&qty_min={self.qty_min}"
        url += f"&qty_max={self.qty_max}"
        url += f"&amount_min={self.amount_min}"
        url += f"&amount_max={self.amount_max}"
        url += f"&uusd_min={self.uusd_min}"
        url += f"&uusd_max={self.uusd_max}"
        # Thêm giá trị start động
        url += f"&tag_id=0&start={i * 20}"

        return url

    def get_bill_id(self, i: int):
        url = self.generate_url(i)
        re_request = 0
        max_retries = 5
        timeout_seconds = 10
        response: requests.Response
        while re_request < max_retries:
            try:
                response = requests.get(url, headers=self.header, timeout=timeout_seconds)
                soup = BeautifulSoup(response.text, 'html.parser')
                temp_bill_id = soup.find_all("tr")
                # Kiểm tra dữ liệu trả về
                bill_expect = 21 if i != self.final_page else self.expect_bill_of_final_page+1
                if temp_bill_id is None or len(temp_bill_id) < bill_expect  :
                    print(f"\nDữ liệu không đủ, thử lại tại trang {i}, Lần {re_request + 1}")
                    if temp_bill_id is not None:
                        print(f"Dữ liệu tại trang {i} là: {len(temp_bill_id)}")
                    re_request += 1
                    self.handle_get_bill_id_failed(url)
                    r = requests.get(url, headers=self.header, timeout=timeout_seconds)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    temp_bill_id = soup.find_all("tr")
                # Sử dụng lock để đảm bảo thread-safe
                with self.lock:
                    for row in temp_bill_id[1:]:
                        billid_value = row.get('data-billid', '').replace('\\"', '')
                        if billid_value and billid_value not in self.bill_ids:
                            self.bill_ids.append(billid_value)
                            self.trade_dates.append(row.get('data-date', '').replace('\\"', ''))
                            self.bill_id_headers.append(url)
                    print(f"Số lượng temp_bill_id: {len(temp_bill_id)}, Số lượng bill_id: {len(self.bill_ids)}, Trang {i}")

                    # Dừng nếu đã đủ số lượng
                    if len(self.bill_ids) >= self.total_bill:
                        print(f"Đã thu thập đủ bill_id trên trang {i}.")
                        return

                break  # Thoát vòng lặp nếu thành công

            except (requests.exceptions.RequestException, TypeError, ConnectionError) as e:
                print(f"Lỗi tại trang {i}, loại lỗi: {e}. Lần thử {re_request + 1}")
                re_request += 1
                if re_request < max_retries:
                    self.handle_get_bill_id_failed(url)
                else:
                    print("Thử lại nhiều lần không thành công, dừng yêu cầu.")
                    self.error_bill_ids.append(i)
                    break

    def handle_get_bill_id_failed(self, url_total):
        print("Get lại header")
        headers_get_delay = perf_counter() - self.start
        if headers_get_delay > 6:
            self.header = headers_get(url_total)
        else:
            sleep(headers_get_delay)
            self.header = headers_get(url_total)

    def start_get_bill_id(self):
        attempt = 0
        max_attempts = 5  # Giới hạn số lần reset cookie
        while len(self.bill_ids) < self.total_bill and attempt < max_attempts:
            print(f"Số lượng bill_id hiện tại: {len(self.bill_ids)}. Yêu cầu: {self.total_bill}")
            attempt += 1
            # Chạy lại việc lấy bill_id với các URL, nhưng dừng khi đủ số lượng
            self.header = get_cookies()
            with ThreadPoolExecutor() as executor:
                # Tạo các task cho từng URL
                futures = [executor.submit(self.get_bill_id, i) for i in self.pages]
                # Chờ tất cả các task hoàn thành
                for future in futures:
                    future.result()
    def execute(self):
        self.start_get_bill_id()
        if len(self.bill_ids) < self.total_bill:
            with ThreadPoolExecutor() as executor:
                executor.map(self.get_bill_id, self.error_bill_ids)
        if len(self.bill_ids) < self.total_bill :
            raise Exception("Cannot get full bill id")




