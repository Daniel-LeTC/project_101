from time import perf_counter

import os
from dotenv import load_dotenv
import csv

from get_bill_detail_process import  GetBillDetailProcess
from login import login
from search_builder import SearchBuilder
from get_bill_id_process_builder import GetBillIDProcessBuilder
from util import import_dict_convert, total_columns, raw_import_header

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
        get_bill_id_process = GetBillIDProcessBuilder(total_bill).set_date_range(start_date,end_date).set_hscode(hs).build()
        get_bill_id_process.execute()

        # tạo file csv để caching data trong quá trình GetBillDetailimport csv
        file_name = f'cahing_data{start_date}_to_{end_date}_{hs}_{trans_type}.csv'
        file = open(file_name, 'w', newline='')  # Thêm newline=''
        file_writer = csv.writer(file)
        # Thêm header vào trước để khi thêm dữ liệu vào csv không bị lệch cột
        file_writer.writerow(raw_import_header)

        file.close()
        print()
        get_detail_process = GetBillDetailProcess(get_bill_id_process.bill_ids,
                                                  get_bill_id_process.trade_dates,
                                                  get_bill_id_process.bill_id_headers,
                                                  file_name)
        get_detail_process.execute()
    print(f"total time consuming: {perf_counter() - start}s")


