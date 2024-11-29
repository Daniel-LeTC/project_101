from get_bill_id_process import GetBillIDProcess
from login import login
from  dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env')
if __name__ == '__main__':
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    print(f"{username}, {password}")
    login(username,password)
    # get_bill_id_process = GetBillIDProcess(
    #     start_date='2023-10-02',
    #     end_date = '2023-10-10',
    #     hs_code = "54",
    #     transaction_type = "import"
    # )
    # get_bill_id_process.execute()




