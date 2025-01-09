from time import perf_counter, sleep
from header import headers_get, get_cookies
import requests
import pandas as pd
import json
from login import logout_then_login


class GetBillDetailProcess:
    def __init__(self,bill_ids,trade_dates,bill_id_headers):
        self.bill_ids = bill_ids
        self.trade_dates = trade_dates
        self.bill_id_headers = bill_id_headers
        self.headers = get_cookies()
        self.bills :pd.DataFrame = pd.DataFrame()
        self.total_bills = 0

    def generate_url(self,j):
        url = "https://en.52wmb.com/async/raw/bill/detail?id="
        url += f"{str(self.bill_ids[j])}"
        url += f"&ie=0&trade_date={str(self.trade_dates[j])}&country=vietnam&ptoken="
        return url

    def get_bill_detail(self, j: int):
        flag = 0
        url_bill = self.generate_url(j)
        print(f"Fetching bill details for bill_id[{j}]: {self.bill_ids[j]}, trade_date[{j}]: {self.trade_dates[j]}")
        print(f"URL: {url_bill}")

        check_headers = True
        re_request = 0
        request_start_time = perf_counter()  # Record start time of the request

        while check_headers:
            try:
                resp = requests.get(url_bill, headers=self.headers, timeout=5)
                df = json.loads(resp.text)  # Convert response JSON to a dictionary
                print(df)
                df_1 = pd.json_normalize(df["data"]["detail"])  # Normalize the details into a DataFrame

                # Check if the dataframe has sufficient columns, retry if not
                if len(df_1.columns) < 10:
                    raise ValueError("Insufficient data, retrying...")

                return df_1  # Return the fetched DataFrame
            except Exception as e:
                if e is KeyError:
                    print(f"Error: {e}")
                    state = df["state"]
                    if  state == 3001 :
                        if flag > 2 :
                            logout_then_login()
                        else:
                            print(f"Số lần bị state = 3001 : {flag}")
                            flag = flag + 1
                if perf_counter() - request_start_time > 6:  # If request takes more than 6 seconds
                    self.headers = headers_get(self.bill_id_headers[j])  # Refresh headers
                else:
                    sleep(perf_counter() - request_start_time)  # Sleep for 6 seconds before retrying
                    re_request = re_request + 1
                if re_request >= 20:  # Break after 20 retries
                        break

    def run_get_bill_detail(self):
        # Loop through each bill_id
        for self.total_bills in range(len(self.bill_ids)):
            print(f"Processing bill_id[{self.total_bills}]: {self.bill_ids[self.total_bills]}")
            df_1 = self.get_bill_detail(self.total_bills)  # Get bill details

            if df_1 is not None:  # If data is successfully fetched
                self.bills = pd.concat([self.bills, df_1])  # Append to the main DataFrame
                self.total_bills += 1
            else:
                print(f"Failed to fetch data for bill_id[{self.total_bills}]. Skipping.")

            print(f"Current number of bills: {self.bills.shape}, Total bills fetched: {self.total_bills}")
            sleep(0.8)  # Delay between requests to avoid overloading server
        print(f"Total bills fetched: {self.total_bills}, Expected bill count: {len(self.bill_ids)}, Recent data count: {self.bills.shape}")

    def execute(self):
        while self.total_bills < len(self.bill_ids):
            print(self.total_bills)
            self.run_get_bill_detail()
        return self.bills