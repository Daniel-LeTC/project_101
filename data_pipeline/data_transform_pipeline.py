import pandas as pd
import numpy as np
from babel.messages.extract import extract
from util import column_to_keep,import_column_mapping

query = f'''begin;
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

def clean_payment_method_khongtt(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[(df['payment_method'] != 'KHONGTT')]

def clean_weight(df: pd.DataFrame) -> pd.DataFrame:
    df.weight = df.weight.astype('string')
    extracted = df['weight'].str.extract(r'(?P<number>\d+)(?P<unit>\D*)')

    df['weight'] = extracted['number'].astype(float)

    df['weight_unit'] = np.where(
        df['weight_unit'].isna() & extracted['unit'].notna(),
        extracted['unit'].str.strip(),
        df['weight_unit']
    )
    return df

def clean_quantity(df: pd.DataFrame) -> pd.DataFrame:
    df.qty = df.qty.astype('string')
    extracted = df['qty'].str.extract(r'(?P<number>\d+(?:\.\d+)?)(?P<unit>\D*)')
    df['qty'] = extracted['number'].astype(float)

    df['quantity_unit'] = np.where(
        df['quantity_unit'].isna() & extracted['unit'].notna(),
        extracted['unit'].str.strip(),
        df['weight_unit']
    )
    return df

def remove_unused_column(df: pd.DataFrame) -> pd.DataFrame:
    # Lọc các cột nằm trong util.column_to_keep
    columns = column_to_keep
    return df[[column for column in df.columns if column in columns]]
def clean_date_column(df:pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def convert_column(df:pd.DataFrame,columns,type_trans="import"):
    df['transaction_type'] = type_trans
    df.rename(columns=columns,inplace=True)
    return df
def transform_data(filename):
    df = pd.read_csv(f"{filename}.csv")
    pd.options.mode.copy_on_write = True
    df = clean_payment_method_khongtt(df)
    df = clean_weight(df)
    df = clean_quantity(df)
    df = clean_date_column(df)
    df = remove_unused_column(df)
    df = convert_column(df, import_column_mapping)
    # df.to_csv(f"{filename}_transformed_data.csv", index=False)

    return df