from fileinput import filename

import pandas as pd
from .connection import import_csv_to_postgresql

fullpath = "D:/git/project_101/data_pipeline/"

def load_bill_detail_to_db(filename: str):
    global fullpath
    filepath = fullpath + filename
    print(f"Lấy dữ liệu tại file: {filepath}")

    # Xây dựng câu lệnh COPY với đường dẫn đầy đủ
    query = f'''begin transaction isolation level serializable;
    COPY data_crawling2.data_crawling (hs_code, transportation, unit_price_currency, products, trade_date,
    country_of_origin, b_l_number_or_awb_number, total_value_currency, weigh_unit, incoterms, buyer,
    quantity_unit, supplier, declaration_number, import_tax, customs, importer_code, total_value_usd,
    buyer_supplier_tel, loading_port, destination_country, unit_price_usd, bill_id, currency,
    flight_voyage_number, fob_usd, buyer_address, cif_usd, quantity, payment_method,
    gross_weight_kg, customs_warehouse_name_in_vietnamese_port, transaction_type)
    FROM '{filepath}'
    DELIMITER ','
    CSV HEADER;
    '''

    # Thực hiện nhập dữ liệu
    response = import_csv_to_postgresql(query)
    if response != "Succeed":
        raise Exception(response)
