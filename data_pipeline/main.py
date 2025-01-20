from time import perf_counter
import os
from dotenv import load_dotenv

from CSV import create_file_data_crawling_if_not_exist
from GetBillDetail import  GetBillDetailProcess
from Authentication import login
from Search import GetTotalBill
from GetBilllID import GetBillIDProcess
from TransformPipeline import transform_data
from Postgre import load_bill_detail_to_db

load_dotenv(dotenv_path='.env')
def manual_pipeline(start_date,end_date,hs,trans_type):
    login(os.getenv('USER_NAME'),os.getenv('PASSWORD'))

    total_bills = GetTotalBill(
        start_date= start_date,
        end_date= end_date,
        hscode= hs,
        transaction_type= trans_type
    ).execute()

    if total_bills !=0:
        get_bill_id_process = GetBillIDProcess(
            start_date=start_date,
            end_date= end_date,
            hscode=hs,
            type_transaction=trans_type,
            total_bill=total_bills)
        get_bill_id_process.execute()

        # tạo file csv để caching data trong quá trình GetBillDetailimport csv
        file_path = f'CSV/Data/{start_date}_to_{end_date}_{hs}_{trans_type}'
        create_file_data_crawling_if_not_exist(f"{file_path}.csv")
        get_detail_process = GetBillDetailProcess(get_bill_id_process.bill_ids,
                                                  get_bill_id_process.trade_dates,
                                                  get_bill_id_process.bill_id_headers,
                                                  f'{file_path}.csv')
        get_detail_process.execute()
        transform_data(file_path)
        r = load_bill_detail_to_db(f'{file_path}_transformed_data.csv')
        if r['state'] != 200:
            print(r['message'])
            return
        print("Lấy dữ liệu thành công")


if __name__ == '__main__':
    # khai báo biến
    start = perf_counter()
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    start_date = "2024-10-28"
    end_date = "2024-12-10"
    hs = "50"
    trans_type = "import"
    # start process
    manual_pipeline(start_date,end_date,hs,trans_type)