import csv
from util import raw_import_header
def create_file_data_crawling_if_not_exist(file_path):
    file = open(f'{file_path}', 'w', newline='')  # Thêm newline=''
    file_writer = csv.writer(file)
    # Thêm header vào trước để khi thêm dữ liệu vào csv không bị lệch cột
    file_writer.writerow(raw_import_header)
    file.close()
    return True