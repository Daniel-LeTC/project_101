from time import perf_counter

from get_bill_id_process import GetBillIDProcess
from login import login
from dotenv import load_dotenv
import os
from search_builder import SearchBuilder
from get_bill_id_process_builder import GetBillIDProcessBuilder
load_dotenv(dotenv_path='.env')

if __name__ == '__main__':
    start = perf_counter()
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    print(f"{username}, {password}")
    login(username,password)
    start_date = "2023-04-20"
    end_date = "2023-04-20"
    hs = "54"
    trans_type = "import"

    total_bill = SearchBuilder()\
                    .set_date_range(start_date,end_date)\
                    .set_hscode(hs)\
                    .get_total_bill()
                    # .set_buyer_port(buyer_port)\



    print(total_bill)


    get_bill_id_process = GetBillIDProcessBuilder(total_bill)\
                            .set_date_range(start_date,end_date)\
                            .set_hscode(hs)\
                            .build()
                            # .set_buyer_port(buyer_port)\

    get_bill_id_process.execute()
    runtime = perf_counter() - start
    print(f"run {runtime}")
