from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from Authentication import Driver
driver = Driver.get_driver()

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from Authentication import Driver

class GetTotalBill:
    def __init__(self, start_date, end_date=None, hscode=None, description=None,
                 supplier=None, buyer=None, seller_country=None, seller_port=None,
                 buyer_port=None, trans=None, qty_min=None, qty_max=None,
                 amount_min=None, amount_max=None, uusd_min=None, uusd_max=None,
                 transaction_type="import"):
        """
        Khởi tạo với tất cả các tham số cần thiết.
        """
        self.driver = Driver.get_driver()
        self.start_date = start_date
        self.end_date = end_date or start_date
        self.hscode = hscode
        self.description = description
        self.supplier = supplier
        self.buyer = buyer
        self.seller_country = seller_country
        self.seller_port = seller_port
        self.buyer_port = buyer_port
        self.trans = trans
        self.qty_min = qty_min
        self.qty_max = qty_max
        self.amount_min = amount_min
        self.amount_max = amount_max
        self.uusd_min = uusd_min
        self.uusd_max = uusd_max
        self.transaction_type = transaction_type

    def process_field(self, field_xpath, value):
        """
        Kiểm tra giá trị không null, sau đó xử lý nhập liệu vào trường trên giao diện.
        """
        if value:
            element = self.driver.find_element(By.XPATH, field_xpath)
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
            element.send_keys(value)

    def execute(self):
        """
        Thực hiện thao tác tìm kiếm và trả về tổng số lượng bill.
        """
        # Truy cập trang web
        self.driver.get('https://en.52wmb.com/customs-data/vietnam')
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))
        sleep(2)

        # Nếu cần đổi loại giao dịch
        if self.transaction_type.lower() != "import":
            imex_field = self.driver.find_element(By.XPATH, '//*[@id="search_ie_dropdown"]/div')
            imex_field.click()
            sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="search_ie_dropdown"]/ul/li[2]').click()

        # Map các trường với giá trị tương ứng
        fields = {
            '//*[@id="start_date"]': self.start_date,
            '//*[@id="end_date"]': self.end_date,
            '//*[@id="hs"]': self.hscode,
            '//*[@id="des"]': self.description,
            '//*[@id="seller"]': self.supplier,
            '//*[@id="buyer"]': self.buyer,
            '//*[@id="seller_country"]': self.seller_country,
            '//*[@id="seller_port"]': self.seller_port,
            '//*[@id="buyer_port"]': self.buyer_port,
            '//*[@id="trans"]': self.trans,
            '//*[@id="qty_min"]': self.qty_min,
            '//*[@id="qty_max"]': self.qty_max,
            '//*[@id="amount_min"]': self.amount_min,
            '//*[@id="amount_max"]': self.amount_max,
            '//*[@id="uusd_min"]': self.uusd_min,
            '//*[@id="uusd_max"]': self.uusd_max
        }

        # Điền dữ liệu vào các trường
        for field_xpath, value in fields.items():
            self.process_field(field_xpath, value)

        # Bấm nút tìm kiếm
        self.driver.find_element(By.XPATH, '//*[@id="search_btn"]').click()
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer layui-layer-loading')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-setwin')))
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'layui-layer-shade')))
        sleep(2)

        # Lấy kết quả tổng số lượng bill
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        total_bill = soup.find("span", {"class": "hits"}).get_text(strip=True)
        total_bill = int(total_bill)

        # Xử lý giới hạn số lượng bill
        if total_bill > 10000:
            if self.start_date != self.end_date:
                print("LỖI: Tổng lượng bill không được quá 10k!")
                return 0
            else:
                print("CẢNH CÁO: Total bill đã vượt quá 10k nhưng chỉ lấy được 10k dữ liệu.")
                return 10000

        return total_bill

