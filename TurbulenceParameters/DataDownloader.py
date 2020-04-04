import requests
import re
from datetime import datetime


class DataDownloader:
    def __init__(self):
        self.start_datetime = datetime(2020, 1, 1)
        self.end_datetime = datetime(2020, 1, 1)
        self.binary_data = []
        self.years_flag = 1

    def download_data(self, path='http://amk030.imces.ru/meteodata/AMK_030_BIN/'):
        res = requests.get(path)
        pattern = r"(href=\"[\d\w.%]*[\/]\")"  # Для папок
        folders = re.findall(pattern, res.text)

        if folders:
            if self.years_flag:
                self.years_flag = 0
                for year_folder in folders:
                    if 'T' in year_folder[6:-2]:
                        if int(year_folder[6:-2][4:]) == self.end_datetime.year:
                            print(year_folder[6:-2][4:])
                            self.download_data(path + year_folder[6:-1])
                    elif self.start_datetime.year <= int(year_folder[6:-2]) <= self.end_datetime.year:
                        print(year_folder[6:-2])
                        self.download_data(path + year_folder[6:-1])
            else:
                for month_folder in folders:
                    print(month_folder[6:-1])
                    self.download_data(path + month_folder[6:-1])

        else:
            pattern = r"(href=\"[\d\w.]*B\")"  # для файлов
            files = re.findall(pattern, res.text)
            print(len(files))
            if files:
                for file in files:
                    file = file[6:-1]
                    file_date = datetime.strptime(
                        file[2:4] + '.' + file[:2] + '.20' + file[-3:-1] + ' ' + file[4:6] + ':' + file[6:8],
                        '%d.%m.%Y %H:%M')
                    if file_date > self.end_datetime:
                        return
                    if file_date >= self.start_datetime:
                        print(file)
                        self.binary_data.append(requests.get(path + file).content)
            else:
                return print("В папке", path, "Фалов нет! ")


if __name__ == "__main__":
    downloader = DataDownloader()
    downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
    downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
    downloader.download_data()
    print("Number of files = ", len(downloader.binary_data))
