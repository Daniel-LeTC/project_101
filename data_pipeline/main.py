from time import perf_counter
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


from CSV import create_file_data_crawling_if_not_exist
from GetBillDetail import GetBillDetailProcess
from util import login, TRANSFORMED_DATA_FILE_PATH, RAW_DATA_FILE_PATH, ERROR_HANDLING_FILE_PATH, beep_sound
from Search import GetTotalBill
from GetBilllID import GetBillIDProcess
from TransformPipeline import transform_data
from Postgre import load_bill_detail_to_db

load_dotenv(dotenv_path='.env')

def manual_pipeline(start_date, end_date, hscode, description,
                    supplier, buyer, seller_country, seller_port,
                    buyer_port, trans, qty_min, qty_max,
                    amount_min, amount_max, uusd_min, uusd_max,
                    transaction_type="import"):
    try:
        total_bills = GetTotalBill(
            start_date=start_date,
            end_date=end_date,
            hscode=hscode,
            transaction_type=transaction_type,
            description=description,
            supplier=supplier,
            buyer=buyer,
            seller_port=seller_port,
            seller_country=seller_country,
            buyer_port=buyer_port,
            trans=trans,
            qty_min=qty_min,
            qty_max=qty_max,
            amount_min=amount_min,
            amount_max=amount_max,
            uusd_min=uusd_min,
            uusd_max=uusd_max,
        ).execute()

        if total_bills != 0:
            get_bill_id_process = GetBillIDProcess(
                start_date=start_date,
                end_date=end_date,
                hscode=hscode,
                description=description,
                buyer=buyer,
                seller_port=seller_port,
                seller_country=seller_country,
                buyer_port=buyer_port,
                trans=trans,
                qty_min=qty_min,
                qty_max=qty_max,
                amount_min=amount_min,
                amount_max=amount_max,
                uusd_min=uusd_min,
                uusd_max=uusd_max,
                transaction_type=transaction_type,
                supplier=supplier,
                total_bill=total_bills
            )
            get_bill_id_process.execute()

            # tạo file csv để caching data trong quá trình GetBillDetailimport csv
            create_file_data_crawling_if_not_exist(RAW_DATA_FILE_PATH)
            get_detail_process = GetBillDetailProcess(bill_ids=get_bill_id_process.bill_ids,
                                                      trade_dates=get_bill_id_process.trade_dates,
                                                      bill_id_headers=get_bill_id_process.bill_id_headers)
            get_detail_process.execute()
            if not transform_data():
                return
            load_bill_detail_to_db(TRANSFORMED_DATA_FILE_PATH)

    except :
        transform_data()
        load_bill_detail_to_db(TRANSFORMED_DATA_FILE_PATH)
        beep_sound()

def rerun_pipeline():
    print("Rerun pipeline")
    data = pd.read_csv(ERROR_HANDLING_FILE_PATH)
    GetBillDetailProcess(bill_ids=data['bill_ids'].tolist(),
                                                   trade_dates=data['trade_dates'].tolist(),
                                                   bill_id_headers=data['bill_id_headers'].tolist()).execute()
    transform_data()
    load_bill_detail_to_db(TRANSFORMED_DATA_FILE_PATH)


if __name__ == '__main__':
    # khai báo biến
    start = perf_counter()

    start_date = "2024-10-28"
    end_date = "2024-12-10"
    hs = "50"
    description = None
    supplier = None
    buyer = None
    seller_port = None
    seller_country = None
    buyer_port = None
    trans = None
    qty_min = None
    qty_max = None
    amount_min = None
    amount_max = None
    uusd_min = None
    uusd_max = None
    transaction_type = None
    login()
    # start process
    error_handling_file_path = Path(ERROR_HANDLING_FILE_PATH)
    if not error_handling_file_path.exists():
        manual_pipeline(
            start_date=start_date,
            end_date=end_date,
            hscode=hs,
            description=description,
            supplier=supplier,
            buyer=buyer,
            seller_port=seller_port,
            buyer_port=buyer_port,
            trans=trans,
            qty_min=qty_min,
            qty_max=qty_max,
            amount_min=amount_min,
            amount_max=amount_max,
            uusd_min=uusd_min,
            uusd_max=uusd_max,
            seller_country=seller_country,
            transaction_type=transaction_type
        )
    else:
        rerun_pipeline()

