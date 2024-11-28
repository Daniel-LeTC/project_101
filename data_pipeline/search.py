from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from driver import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class Search():
    def __init__(self):
        self.driver = Driver.get_driver()
    def start_search(self,start_date,end_date,hscode,type_transaction):
        Buyer = ""
        Supplier = ""
        Des = ""

        ############################################################
        self.driver.get('https://en.52wmb.com/customs-data/vietnam')
        # driver.refresh()
        # sleep(1)

        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))
        sleep(2)

        if type_transaction == "import":
            imex_field = self.driver.find_element('xpath', '//*[@id="search_ie_dropdown"]/div')
            imex_field.click()
            sleep(1)
        elif type_transaction == "export":
            ex_field = self.driver.find_element('xpath', '//*[@id="search_ie_dropdown"]/ul/li[2]').click()

        # sleep(10)
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-setwin')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))
        sleep(2)

        # HS field
        HS_field = self.driver.find_element('xpath', '//*[@id="hs"]').send_keys(str(hscode))

        # Des field
        Des_field = self.driver.find_element('xpath', '//*[@id="des"]').send_keys(str(Des))

        # Start date field
        startdate_field = self.driver.find_element('xpath', '//*[@id="start_date"]').send_keys(Keys.CONTROL + 'a',
                                                                                          Keys.DELETE)
        startdate_field = self.driver.find_element('xpath', '//*[@id="start_date"]').send_keys(start_date)

        # End date field
        enddate_field = self.driver.find_element('xpath', '//*[@id="end_date"]').send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        enddate_field = self.driver.find_element('xpath', '//*[@id="end_date"]').send_keys(str(end_date))

        # Buyer field
        buyer_field = self.driver.find_element('xpath', '//*[@id="buyer"]').send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        buyer_field = self.driver.find_element('xpath', '//*[@id="buyer"]').send_keys(Buyer)

        # Supplier field
        supplier_field = self.driver.find_element('xpath', '//*[@id="seller"]').send_keys(Keys.CONTROL + 'a', Keys.DELETE)
        supplier_field = self.driver.find_element('xpath', '//*[@id="seller"]').send_keys(Supplier)

        sleep(2)

        # Search field
        search_field = self.driver.find_element('xpath', '//*[@id="search_btn"]').click()

        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-setwin')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))

        sleep(2)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        total_bill = soup.find("span", {"class": "hits"}).get_text(strip=True)
        total_bill = int(total_bill)
        print(total_bill)
        return  total_bill

    def genarate_url(self,bill_id ,tradedate):
        return f"https://en.52wmb.com/async/raw/bill/detail?id={bill_id}&ie=1&trade_date={tradedate}&country=vietnam&ptoken="
