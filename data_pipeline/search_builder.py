from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver import Driver
from get_bill_id_process import GetBillIDProcess
from time import sleep
class SearchBuilder:
    def __init__(self):
        self.driver = Driver.get_driver()
        self.fields = {}
        self.unfold = False
    def set_date_range(self, start_date, end_date=""):
        self.fields['//*[@id="start_date"]'] = start_date
        final_end_date = start_date if end_date == "" else end_date
        self.fields['//*[@id="end_date"]'] = final_end_date
        return self

    def set_hscode(self, hscode):
        self.fields['//*[@id="hs"]'] = hscode
        return self

    def set_description(self, description):
        self.fields['//*[@id="des"]'] = description
        return self

    def set_supplier(self, supplier):
        self.fields['//*[@id="seller"]'] = supplier
        return self

    def set_buyer(self, buyer):
        self.fields['//*[@id="buyer"]'] = buyer
        return self

    def set_seller_country(self, seller_country):
        self.fields['//*[@id="seller_country"]'] = seller_country
        return self

    def set_seller_port(self, seller_port):
        self.fields['//*[@id="seller_port"]'] = seller_port
        return self

    def set_buyer_port(self, buyer_port):
        
        self.fields['//*[@id="buyer_port"]'] = buyer_port
        return self

    def set_trans(self, trans):
        
        self.fields['//*[@id="trans"]'] = trans
        return self

    def set_qty_min(self, qty_min):
        
        self.fields['//*[@id="qty_min"]'] = qty_min
        return self

    def set_qty_max(self, qty_max):
        
        self.fields['//*[@id="qty_max"]'] = qty_max
        return self

    def set_amount_min(self, amount_min):
        
        self.fields['//*[@id="amount_min"]'] = amount_min
        return self

    def set_amount_max(self, amount_max):
        
        self.fields['//*[@id="amount_max"]'] = amount_max
        return self

    def set_uusd_min(self, uusd_min):
        
        self.fields['//*[@id="uusd_min"]'] = uusd_min
        return self

    def set_uusd_max(self, uusd_max):
        
        self.fields['//*[@id="uusd_max"]'] = uusd_max
        return self

    def unfold_search(self):
        self.driver.find_element('xpath', '//*[@id="higher_search"]').click()

    def get_total_bill(self):
        # load trang search
        self.driver.get('https://en.52wmb.com/customs-data/vietnam')
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading'))
        )
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade'))
        )
        sleep(2)
        # Nếu có trường nằm trong phần search mở rộng thì mở rộng

        self.unfold_search()

        for field,value in self.fields.items():
            element = self.driver.find_element(By.XPATH, field)
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
            element.send_keys(value)

        # bấm nút search
        self.driver.find_element('xpath', '//*[@id="search_btn"]').click()
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-setwin')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))
        sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        total_bill = soup.find("span", {"class": "hits"}).get_text(strip=True)
        total_bill = int(total_bill)
        print(total_bill)
        return total_bill

