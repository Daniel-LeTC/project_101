from get_bill_id_process import GetBillIDProcess
from login import login
from dotenv import load_dotenv
import os
from search_builder import SearchBuilder

load_dotenv(dotenv_path='.env')
if __name__ == '__main__':
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    print(f"{username}, {password}")
    login(username,password)
    SearchBuilder()\
        .set_date_range("2023-08-31","2024-08-31")\
        .set_hscode("54")\
        .set_buyer_port("GUANGXI PINGXIANG GUANGFENG IMPORT AND EXPORT TRADE CO., LTD")\
        .start_search()



