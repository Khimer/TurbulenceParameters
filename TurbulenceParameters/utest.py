import unittest
from TurbulenceParameters.BytesParser import *
from TurbulenceParameters.DataDownloader import *
from TurbulenceParameters.ParametersCalculator import *
from TurbulenceParameters.CsvWriter import *


class DownloaderTest(unittest.TestCase):

    # def test_parse(self):
    #     downloader = DataDownloader()
    #     downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
    #     downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
    #     downloader.download()
    #     parser = BytesParser()
    #     data = parser.parse(downloader.binary_data[0])
    #     for binary_file in downloader.binary_data[1:]:
    #         data = np.append(data, parser.parse(binary_file), axis=1)
    #     self.assertEqual(data.shape[0], 7)
    #
    # def test_check(self):
    #     self.assertEqual(type([]), list)
    # def test_puk(self):
    #     self.assertEqual(type('[]'), str)
    #
    # def test_download(self):
    #     downloader = DataDownloader()
    #     downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
    #     downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
    #     downloader.download()
    #     self.assertEqual(type(downloader.binary_data), list)

    def test_all(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        parser = BytesParser()
        data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            data = np.append(data, parser.parse(binary_file), axis=1)
        calculator = ParametersCalculator()
        print(calculator.calculate(data))
        writer = CsvWriter()
        writer.save_csv(data, 'babaka')




if __name__ == "__main__":
    unittest.main()