import pandas as pd
import numpy as np
from util import column_to_keep, import_column_mapping, RAW_DATA_FILE_PATH, TRANSFORMED_DATA_FILE_PATH


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
def transform_data():
    try:
        df = pd.read_csv(RAW_DATA_FILE_PATH)
        pd.options.mode.copy_on_write = True
        df = clean_payment_method_khongtt(df)
        df = clean_weight(df)
        df = clean_quantity(df)
        df = clean_date_column(df)
        df = remove_unused_column(df)
        df = convert_column(df, import_column_mapping)
        df.to_csv(TRANSFORMED_DATA_FILE_PATH, index=False)
        return True
    except Exception as e :
        print(f"Error occur when transform data : {e}")
        return False
