from TurbulenceParameters.BytesParser import *
from TurbulenceParameters.DataDownloader import *
from TurbulenceParameters.ParametersCalculator import *
from TurbulenceParameters.CsvWriter import *
from TurbulenceParameters.CsvReader import *
from TurbulenceParameters.DataAggregator import *


class Service:
    def __init__(self):
        self.data = 0
        self.connection = 0
        self.availableTimeStart = 0
        self.availableTimeEnd = 0
        self.parser = BytesParser()
        self.reader = CsvReader()
        self.writer = CsvWriter()
        self.calculator = ParametersCalculator()
        self.aggregator = DataAggregator()
        self.downloader = DataDownloader()

    def check_connection_and_time_range(self):
        def get_time(index):
            path = 'http://amk030.imces.ru/meteodata/AMK_030_BIN/'
            answer = requests.get(path)
            pattern = r"(href=\"[\d\w.%]*[\/]\")"  # Для папок
            folders = re.findall(pattern, answer.text)
            position = folders[index][6:-1]
            position = path + position
            if index == 0:
                answer = requests.get(position)
                folders = re.findall(pattern, answer.text)
                print(folders)
                position = position + folders[index][6:-2]
            answer = requests.get(position)
            pattern = r"(href=\"[\d\w.]*B\")"  # для файлов
            files = re.findall(pattern, answer.text)
            file = files[index][6:-1]
            time_date = datetime.strptime(
                file[2:4] + '.' + file[:2] + '.20' + file[-3:-1] + ' ' + file[4:6] + ':' + file[6:8], '%d.%m.%Y %H:%M')
            return time_date

        if requests.get('http://amk030.imces.ru/meteodata/AMK_030_BIN/').status_code == 200:
            self.connection = 1
            self.availableTimeStart = get_time(0)
            self.availableTimeEnd = get_time(-1)

    def set_time_range(self, time_range):
        self.downloader.start_datetime = time_range[0]
        self.downloader.end_datetime = time_range[1]

    def set_constants(self, constants):
        self.calculator.constants = constants

    def set_amount_aggregated_data(self, amount_aggregated_data):
        self.aggregator.amountAggregatedData = amount_aggregated_data

    def get_list_files(self):
        pass

    def download_data(self):
        pass

    def aggregate_data(self, data):
        pass

    def save_data(self, data, selected_time_range):
        pass

    def read_data(self, name_file):
        pass

    def calculate_turbulence_parameters(self):
        pass
