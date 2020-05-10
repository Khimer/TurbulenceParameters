import unittest
from TurbulenceParameters.BytesParser import *
from TurbulenceParameters.DataDownloader import *
from TurbulenceParameters.ParametersCalculator import *
from TurbulenceParameters.CsvWriter import *
from TurbulenceParameters.CsvReader import *
from TurbulenceParameters.DataAggregator import *


# class DownloaderTest(unittest.TestCase):
#
#     def test_download(self):
#         downloader = DataDownloader()
#         downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
#         downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
#         downloader.download()
#         self.assertGreater(len(downloader.binary_data), 0)
#
# class ParserTest(unittest.TestCase):
#
#     def setUp(self):
#         self.downloader = DataDownloader()
#         self.downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
#         self.downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
#         self.downloader.download()
#
#     def test_parse(self):
#         parser = BytesParser()
#         data = parser.parse(self.downloader.binary_data[0])
#         for binary_file in self.downloader.binary_data[1:]:
#             data = np.append(data, parser.parse(binary_file), axis=1)
#         self.assertEqual(data.shape[0], 7)
#
#
# class ReaderTest(unittest.TestCase):
#
#     def test_read(self):
#         reader = CsvReader()
#         self.assertEqual(reader.read('testfile').shape[0], 7)
#
#
# class WriterTest(unittest.TestCase):
#
#     def setUp(self):
#         self.reader = CsvReader()
#         self.data = self.reader.read('testfile')
#
#     def test_write(self):
#         writer = CsvWriter()
#         writer.save_csv(self.data, 'new_file')
#         self.assertIn('new_file', os.listdir(path="."))
#
#
# class AggregatorTest(unittest.TestCase):
#
#     def setUp(self):
#         self.reader = CsvReader()
#         self.data = self.reader.read('testfile')
#
#     def test_aggregate(self):
#         aggregator = DataAggregator()
#         aggregated_data = aggregator.aggregate(self.data)
#         self.assertEqual(aggregated_data.shape[1], self.data.shape[1]//5)
#
#     class CalculatorTest(unittest.TestCase):
#
#         def setUp(self):
#             self.reader = CsvReader()
#             self.data = self.reader.read('testfile')
#
#         def test_calculate(self):
#             calculator = ParametersCalculator()
#             self.assertGreater(len(calculator.calculate(self.data)), 0)

class CommonTest(unittest.TestCase):

    def test_all(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        self.assertGreater(len(downloader.binary_data), 0)

        parser = BytesParser()
        data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            data = np.append(data, parser.parse(binary_file), axis=1)
        self.assertEqual(data.shape[0], 7)

        aggregator = DataAggregator()
        aggregated_data = aggregator.aggregate(data)
        print(aggregated_data.shape, data.shape)
        self.assertEqual(aggregated_data.shape[1], data.shape[1] // 100)

        calculator = ParametersCalculator()
        calculator.calculate(aggregated_data)
        self.assertGreater(len(calculator.calculate(data)), 0)

        writer = CsvWriter()
        writer.save_csv(aggregated_data, 'test_file')
        self.assertIn('test_file.csv', os.listdir(path="."))

        reader_tmp = CsvReader()
        self.assertEqual(reader_tmp.read('test_file.csv').shape[0], 7)


if __name__ == "__main__":
    unittest.main()
