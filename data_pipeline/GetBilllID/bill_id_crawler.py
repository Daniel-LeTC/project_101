from concurrent.futures.thread import ThreadPoolExecutor

from util import get_cookies


class BillIDCrawler:
    def __init__(self, processor):
        self.processor = processor

    def fetch_bill_ids(self, max_attempts=5):
        raise NotImplemented("Hàm phải được định nghĩa trong subclass")
