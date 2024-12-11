from get_bill_id_process import GetBillIDProcess

class GetBillIDProcessBuilder:
    def __init__(self,total_bill:int):
        self.get_bill_id_process = GetBillIDProcess(total_bill)

    def set_date_range(self, start_date,end_date=""):
        self.get_bill_id_process.start_date = start_date
        self.get_bill_id_process.end_date = start_date if end_date == "" else end_date
        return self

    def set_hscode(self, hscode):
        self.get_bill_id_process.hscode = hscode
        return self

    def set_transaction_type(self, transaction_type):
        self.get_bill_id_process.type_transaction = transaction_type
        return self

    def set_supplier(self, supplier):
        self.get_bill_id_process.supplier = supplier
        return self

    def set_buyer(self, buyer):
        self.get_bill_id_process.buyer = buyer
        return self

    def set_description(self, description):
        self.get_bill_id_process.des = description
        return self

    def set_seller_country(self, seller_country):
        self.get_bill_id_process.seller_country = seller_country
        return self

    def set_seller_port(self, seller_port):
        self.get_bill_id_process.seller_port = seller_port
        return self

    def set_buyer_port(self, buyer_port):
        self.get_bill_id_process.buyer_port = buyer_port
        return self

    def set_trans(self, trans):
        self.get_bill_id_process.trans = trans
        return self

    def set_qty_min(self, qty_min):
        self.get_bill_id_process.qty_min = qty_min
        return self

    def set_qty_max(self, qty_max):
        self.get_bill_id_process.qty_max = qty_max
        return self

    def set_amount_min(self, amount_min):
        self.get_bill_id_process.amount_min = amount_min
        return self

    def set_amount_max(self, amount_max):
        self.get_bill_id_process.amount_max = amount_max
        return self

    def set_uusd_min(self, uusd_min):
        self.get_bill_id_process.uusd_min = uusd_min
        return self

    def set_uusd_max(self, uusd_max):
        self.get_bill_id_process.uusd_max = uusd_max
        return self


    def build(self):
        return self.get_bill_id_process