from time import perf_counter

import os
from dotenv import load_dotenv

from get_bill_detail_process import  GetBillDetailProcess
from login import login
from search_builder import SearchBuilder
from get_bill_id_process_builder import GetBillIDProcessBuilder
from transform_pipeline import execute_transformations
from util import import_dict_convert

load_dotenv(dotenv_path='.env')

if __name__ == '__main__':
    start = perf_counter()
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    print(f"{username}, {password}")
    login(username,password)
    start_date = "2024-08-31"
    end_date = "2024-08-31"
    hs = "54"
    trans_type = "import"

    total_bill = SearchBuilder().set_date_range(start_date,end_date).set_hscode(hs).get_total_bill(trans_type)

    if total_bill !=0:
        get_bill_id_process = GetBillIDProcessBuilder(total_bill).set_date_range(start_date,end_date)\
                                .set_hscode(hs)\
                                .build()
        get_bill_id_process.execute()

        get_detail_process = GetBillDetailProcess(get_bill_id_process.bill_ids,
                                                  get_bill_id_process.trade_dates,
                                                  get_bill_id_process.bill_id_headers)
        get_detail_process.execute()
    print(f"total time consuming: {perf_counter() - start}s")
        # raw_data =get_detail_process.execute()
        # raw_data.to_excel('raw_data.xlsx',sheet_name='raw_data')
        # transformed_data = execute_transformations(raw_data)
        # transformed_data.to_excel('transformed_data.xlsx',sheet_name='transformed_data')

