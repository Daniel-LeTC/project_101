from GetBilllID.get_bill_id_over_10k import GetBillIDOver10k
from GetBilllID.get_bill_id_under_or_equal_10k import GetBillIDUnderOrEqual10k


class BillIDFactory:
    @staticmethod
    def get_crawler(processor):
        if processor.total_bills <= 10000:
            return GetBillIDUnderOrEqual10k(processor)
        return GetBillIDOver10k(processor)
