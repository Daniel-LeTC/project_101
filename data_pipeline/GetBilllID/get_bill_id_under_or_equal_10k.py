from concurrent.futures.thread import ThreadPoolExecutor

from GetBilllID.bill_id_crawler import BillIDCrawler
from util import get_cookies


class GetBillIDUnderOrEqual10k(BillIDCrawler):
    def __init__(self, processor):
        super().__init__(processor)
        self.processor.final_page = (processor.total_bills // 20) + 1
        self.processor.expect_bill_of_final_page = processor.total_bills % 20
        self.processor.pages = range(0, self.processor.final_page, 1)
        print("Khởi tạo proccessor để get bill_id nhỏ hơn hoặc bằng 10k bill")

    def start_get_bill_id(self):
        """
        Lấy bill_id cho trường hợp dưới hoặc bằng 10k bill.
        """
        with ThreadPoolExecutor() as executor:
            executor.map(self.processor.get_bill_id, self.processor.pages)

        self.fetch_bill_ids()  # Gọi hàm chung để lấy bill_id

    def fetch_bill_ids(self, max_attempts=5):
        """
        Chạy lại quá trình lấy bill ID cho đến khi đạt đủ tổng bill hoặc hết số lần thử lại.
        """
        attempt = 0
        while len(self.processor.bill_ids) < self.processor.total_bills and attempt < max_attempts:
            print(f"Số lượng bill_id hiện tại: {len(self.processor.bill_ids)}/{self.processor.total_bills}")
            attempt += 1

            # Cập nhật header với cookie mới
            self.processor.header = get_cookies()

            with ThreadPoolExecutor() as executor:
                # Tạo các task cho từng URL
                futures = [executor.submit(self.processor.get_bill_id, i) for i in self.processor.pages]

                # Chờ tất cả các task hoàn thành
                for future in futures:
                    future.result()