import os
import threading
from queue import Queue
from time import perf_counter, sleep
from util import headers_get, get_cookies
import requests
import pandas as pd
import json
from util.login import logout_then_login
from util import raw_import_header
from util import ERROR_HANDLING_FILE_PATH,RAW_DATA

class GetBillDetailProcess:
    def __init__(self,bill_ids,trade_dates,bill_id_headers):
        self.bill_ids = bill_ids
        self.trade_dates =  trade_dates
        self.bill_id_headers = bill_id_headers
        self.headers = get_cookies()
        self.bills: pd.DataFrame = pd.DataFrame()
        self.total_bills = 0
        self.queue = Queue()
        self.lock = threading.Lock()  # Lock to handle shared resources
        self.isBreak = False
    def generate_url(self, j):
        url = "https://en.52wmb.com/async/raw/bill/detail?id="
        url += f"{str(self.bill_ids[j])}"
        url += f"&ie=0&trade_date={str(self.trade_dates[j])}&country=vietnam&ptoken="
        return url

    def handle_break_exception(self,index):
        bill_ids = self.bill_ids[index:]
        trade_dates = self.trade_dates[index:]
        bill_id_headers = self.bill_id_headers[index:]
        data_to_write = pd.DataFrame({
            "bill_ids": bill_ids,
            "trade_dates": trade_dates,
            "bill_id_headers" : bill_id_headers,
        })
        data_to_write.to_csv(ERROR_HANDLING_FILE_PATH, index=False)
        self.isBreak = True

    def get_bill_detail(self, j: int):
        flag = 0
        url_bill = self.generate_url(j)
        print(f"Fetching bill details for bill_id[{j}]: {self.bill_ids[j]}, trade_date[{j}]: {self.trade_dates[j]}")
        print(f"URL: {url_bill}")

        check_headers = True
        re_request = 0
        request_start_time = perf_counter()

        while check_headers:
            try:
                resp = requests.get(url_bill, headers=self.headers, timeout=5)
                df = json.loads(resp.text)
                print(df)
                df_1 = pd.json_normalize(df["data"]["detail"])

                if len(df_1.columns) < 10:
                    raise ValueError("Insufficient data, retrying...")

                return df_1
            except Exception as e:
                #handle exception response {staet}
                if isinstance(e, KeyError):
                    print(f"Error: {e}")
                    state = df["state"]
                    if state == 3001:
                        if flag > 2:
                            logout_then_login()
                        else:
                            print(f"Số lần bị state = 3001 : {flag}")
                            flag += 1
                #handle request_
                if perf_counter() - request_start_time > 6:
                    self.headers = headers_get(self.bill_id_headers[j])
                else:
                    sleep(perf_counter() - request_start_time)
                    re_request += 1
                if re_request >= 20:
                    return None
            except KeyboardInterrupt as e:
                self.handle_break_exception(j)



    def run_get_bill_detail(self):
        for j in range(len(self.bill_ids)):
            df_1 = self.get_bill_detail(j)
            if df_1 is not None:
                with self.lock:  # Acquire lock to safely update shared resources
                    self.bills = pd.concat([self.bills, df_1])
                    self.queue.put(df_1)  # Add to queue for CSV thread processing
            else:
                self.handle_break_exception(j)
                break
            sleep(0.8)


    def process_and_save_bills(self):
        while True:
            try:
                df = self.queue.get(timeout=5)  # Wait for data from queue
                if df is not None:
                    # Ensure the columns match the header
                    df = df.reindex(columns=raw_import_header, fill_value="")

                    # Append to CSV without adding header if file exists
                    df.to_csv(RAW_DATA, mode="a", index=False, header=False)

                    with self.lock:
                        self.bills = self.bills.iloc[0:0]  # Clear bills DataFrame
                    print("Data saved and cleared.")
            except:
                print("No data to process. Waiting...")

    def execute(self):
        fetch_thread = threading.Thread(target=self.run_get_bill_detail)
        save_thread = threading.Thread(target=self.process_and_save_bills, daemon=True)

        fetch_thread.start()
        save_thread.start()

        fetch_thread.join()
        if not self.isBreak and os.path.exists(ERROR_HANDLING_FILE_PATH):
            os.remove(ERROR_HANDLING_FILE_PATH)
        print("Fetching complete. Waiting for saving thread to finish.")

