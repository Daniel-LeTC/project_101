from concurrent.futures.thread import ThreadPoolExecutor
from datetime import timedelta, datetime
from math import ceil
from platform import processor
from urllib import parse
from GetBilllID.bill_id_crawler import BillIDCrawler
from util import get_cookies


def calculate_mid_date( start_date, end_date):
    """
    Tính ngày giữa giữa start_date và end_date.
    """
    total_days = (end_date - start_date).days
    mid = start_date + timedelta(days=total_days // 2)
    return mid


def next_day(date):
    """
    Trả về ngày tiếp theo.
    """
    return date + timedelta(days=1)


def previous_day(date):
    """
    Trả về ngày trước đó.
    """
    return date - timedelta(days=1)

class GetBillIDOver10k(BillIDCrawler):
    def __init__(self, processor):
        super().__init__(processor)
        self.date_partitions = []
        self.date_bill_over10k = []
        print("Khởi tạo proccessor để get bill_id trên 10k bill")

    def _fast_partition(self, start_date, end_date, threshold, accumulated_bills=0):
        """
        Phân chia khoảng thời gian [start_date, end_date] thành các partition sao cho
        tổng bill của mỗi partition không vượt quá threshold.
        Nếu một ngày đơn lẻ vượt ngưỡng, ngày đó sẽ được cache.
        """
        # Chuyển đổi start_date, end_date từ str sang datetime.date nếu cần
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        total = self.processor.get_total_bills(start_date, end_date)
        if total < threshold:
            self.date_partitions.append([start_date, end_date, total])
            return

        # Nếu chỉ có 1 ngày mà vượt ngưỡng, lưu ngày đó vào cache và không chia nhỏ thêm.
        if start_date == end_date:
            self.date_bill_over10k.append(start_date)
            return

        # Ước tính số partition cần có
        estimated_partitions = ceil(total / threshold)
        total_days = (end_date - start_date).days + 1  # +1 để tính cả ngày bắt đầu
        estimated_length = max(1, total_days // estimated_partitions)  # Đảm bảo estimated_length >= 1
        guess_date = start_date + timedelta(days=estimated_length)
        if guess_date > end_date:
            guess_date = end_date

        # Xác định khoảng tìm kiếm để binary search
        low, high = start_date, end_date
        partition_point = guess_date  # khởi tạo mặc định
        while low <= high:
            mid = calculate_mid_date(low, high)
            current_total = self.processor.get_total_bills(start_date, mid)
            if current_total < threshold:
                partition_point = mid
                low = next_day(mid)
            else:
                high = previous_day(mid)

        partition_total = self.processor.get_total_bills(start_date, partition_point)
        print(f'Thêm khoảng [{start_date},{partition_point}] với tổng bill {partition_total} vào date_partitions')
        self.date_partitions.append([start_date, partition_point, partition_total])

        # Cập nhật lượng bill tích lũy
        accumulated_bills += partition_total
        print(f'Tổng bill tích lũy: {accumulated_bills}/{self.processor.total_bills}')

        # Kiểm tra nếu tổng bill tích lũy đã đạt ngưỡng
        if accumulated_bills >= self.processor.total_bills:
            return

        # Đệ quy cho phần còn lại của khoảng thời gian
        self._fast_partition(next_day(partition_point), end_date, threshold, accumulated_bills)
    def start_get_bill_id(self):
        """
        Chia nhỏ khoảng thời gian và lấy bill_id theo từng partition.
        """
        start_date = self.processor.start_date
        end_date = self.processor.end_date
        threshold = 10000
        attempt = 0
        max_attempts = 5
        accumulated_bills = 0
        cumulative_bills = 0
        self._fast_partition(start_date, end_date, threshold,accumulated_bills)
        total = self.processor.total_bills
        total_bill_recently = 0

        for date_partition in self.date_partitions:
            self.processor.start_date = date_partition[0]
            self.processor.end_date = date_partition[1]
            partition_total_bills = date_partition[2]
            cumulative_bills += partition_total_bills
            self.processor.final_page = (partition_total_bills // 20) + 1
            self.processor.expect_bill_of_final_page = partition_total_bills % 20
            pages = range(0, self.processor.final_page, 1)
            self.fetch_bill_ids(cumulative_bills,pages)  # Gọi hàm chung để lấy bill_id

    def fetch_bill_ids(self, cumulative_bills=0,pages=None):
        while len(self.processor.bill_ids) < cumulative_bills:
            print(f"Số lượng bill_id hiện tại: {len(self.processor.bill_ids)}/{cumulative_bills}")
            print(f"Số lượng bill_id hiện tại: {len(self.processor.bill_ids)}/{self.processor.total_bills}")

            # Cập nhật header với cookie mới
            self.processor.header = get_cookies()

            with ThreadPoolExecutor() as executor:
                # Tạo các task cho từng URL
                futures = [executor.submit(self.processor.get_bill_id, i) for i in pages]
                # Chờ tất cả các task hoàn thành
                for future in futures:
                    future.result()

