from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import sleep, perf_counter

from bs4 import BeautifulSoup
import urllib.parse
import requests

from driver import Driver
from header import headers_get
from request_handler import RequestHandler
request_handler = RequestHandler()
driver = Driver.get_driver()
lock = Lock()
class GetBillIDProcess:
    def __init__(self,total_bill:int):
        self.start_date = ""
        self.end_date = ""
        self.hscode = ""
        self.type_transaction = ""
        self.buyer = ""
        self.seller = ""
        self.des = ""
        self.seller_country = ""
        self.seller_port = ""
        self.buyer_port = ""
        self.trans = ""
        self.qty_min = ""
        self.qty_max = ""
        self.amount_min = ""
        self.amount_max = ""
        self.uusd_min = ""
        self.uusd_max = ""
        self.total_bill = total_bill
        self.pages = range(0, (total_bill//20) + 1, 1)
        self.driver = Driver.get_driver()
        self.lock = Lock()
        self.start = 0
        self.trade_date = []
        self.bill_ids = []
        self.bill_id_headers = []
        self.error_bill_ids = []
        self.isSuccessful = True
        self.header = None


    def generate_url(self, i):
        transaction_type_code = "1" if self.type_transaction == "export" else "0"

        # Khởi tạo URL với các tham số bắt buộc
        url = f"https://en.52wmb.com/async/raw/trade/list?country=vietnam&=undefined&ie={transaction_type_code}"

        # Thêm từng tham số động
        url += f"&start_date={self.start_date}&end_date={self.end_date}"
        url += f"&hs={self.hscode}"
        url += f"&des={urllib.parse.quote(self.des)}"
        url += f"&seller={urllib.parse.quote(self.seller)}"
        url += f"&buyer={urllib.parse.quote(self.buyer)}"
        url += f"&seller_country={urllib.parse.quote(self.seller_country)}"
        url += f"&seller_port={urllib.parse.quote(self.seller_port)}"
        url += f"&buyer_port={urllib.parse.quote(self.buyer_port)}"
        url += f"&trans={self.trans}"
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
        attempt = 0
        url = self.generate_url(i)
        re_request = 0
        max_retries = 5
        timeout_seconds = 10

        while re_request < max_retries:
            try:
                response = requests.get(url, headers=self.header, timeout=timeout_seconds)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                soup = BeautifulSoup(response.text, 'html.parser')
                temp_bill_id = soup.find_all("tr")

                # Kiểm tra dữ liệu trả về
                if not temp_bill_id:
                    print(f"Dữ liệu không đủ, thử lại... Lần {re_request + 1}")
                    re_request += 1
                    self.handle_get_bill_id_failed(url)
                    continue

                # Sử dụng lock để đảm bảo thread-safe
                with self.lock:
                    for row in temp_bill_id[1:]:
                        billid_value = row.get('data-billid', '').replace('\\"', '')
                        if billid_value and billid_value not in self.bill_ids:
                            self.bill_ids.append(billid_value)
                            self.trade_date.append(row.get('data-date', '').replace('\\"', ''))
                            self.bill_id_headers.append(url)

                        # Dừng nếu đã đủ số lượng
                        if len(self.bill_ids) >= self.total_bill:
                            print(f"Đã thu thập đủ bill_id trên trang {i}.")
                            return

                print(f"URL: {url}")
                print(f"Số lượng temp_bill_id: {len(temp_bill_id)}, Số lượng bill_id: {len(self.bill_ids)}, Trang {i}")
                break  # Thoát vòng lặp nếu thành công

            except (requests.exceptions.RequestException, TypeError, ConnectionError) as e:
                print(f"Lỗi tại trang {i}, loại lỗi: {e}. Lần thử {re_request + 1}")
                re_request += 1
                if re_request < max_retries:
                    self.handle_get_bill_id_failed(url)
                else:
                    print("Thử lại nhiều lần không thành công, dừng yêu cầu.")
                    break
            finally:
                print(f"re_request: {re_request}")
        if re_request == max_retries-1:
            self.error_bill_ids.append((i))

    def handle_get_bill_id_failed(self, url_total):
        print("Get lại header")
        headers_get_delay = perf_counter() - self.start
        if headers_get_delay > 6:
            self.header = headers_get(url_total)
        else:
            sleep(headers_get_delay)
            self.header = headers_get(url_total)

    def check_and_reset_cookies(self):
        attempt = 0
        max_attempts = 5  # Giới hạn số lần reset cookie
        while len(self.bill_ids) < self.total_bill and attempt < max_attempts:
            print(f"Số lượng bill_id hiện tại: {len(self.bill_ids)}. Yêu cầu: {self.total_bill}")
            attempt += 1

            # Chạy lại việc lấy bill_id với các URL, nhưng dừng khi đủ số lượng
            with ThreadPoolExecutor() as executor:
                # Tạo các task cho từng URL
                futures = [executor.submit(self.get_bill_id, i) for i in self.pages]
                # Chờ tất cả các task hoàn thành
                for future in futures:
                    future.result()

            if len(self.bill_ids) >= self.total_bill:
                print(f"Đã lấy đủ bill_id ({len(self.bill_ids)}).")
                return

    def execute(self):
        self.check_and_reset_cookies()
        # with ThreadPoolExecutor() as executor:
        #     executor.map(self.get_bill_id, self.pages)