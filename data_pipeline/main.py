from time import perf_counter
import os
from dotenv import load_dotenv

from file_handler import create_file_data_crawling_if_not_exist
from get_bill_detail_process import  GetBillDetailProcess
from login import login
from search_builder import SearchBuilder
from get_bill_id_process_builder import GetBillIDProcessBuilder
from data_transform_pipeline import transform_data

load_dotenv(dotenv_path='.env')

if __name__ == '__main__':
    # khai báo biến
    start = perf_counter()
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    start_date = "2024-08-31"
    end_date = "2024-08-31"
    hs = "54"
    trans_type = "import"
    # start process
    login(username,password)
    total_bill = SearchBuilder().set_date_range(start_date,end_date).set_hscode(hs).get_total_bill(trans_type)

    if total_bill !=0:
        get_bill_id_process = GetBillIDProcessBuilder(total_bill).set_date_range(start_date,end_date).set_hscode(hs).build()
        get_bill_id_process.execute()

        # tạo file csv để caching data trong quá trình GetBillDetailimport csv
        file_name = f'data_crawling_{start_date}_to_{end_date}_{hs}_{trans_type}'
        create_file_data_crawling_if_not_exist(f"{file_name}.csv")
        get_detail_process = GetBillDetailProcess(get_bill_id_process.bill_ids,
                                                  get_bill_id_process.trade_dates,
                                                  get_bill_id_process.bill_id_headers,
                                                  f'{file_name}.csv')
        get_detail_process.execute()
        transform_data(file_name)