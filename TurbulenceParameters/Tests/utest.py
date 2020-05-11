import unittest
import os
from ..TurbulenceParameters.BytesParser import *
from ..TurbulenceParameters.DataDownloader import *
from ..TurbulenceParameters.ParametersCalculator import *
from ..TurbulenceParameters.CsvWriter import *
from ..TurbulenceParameters.CsvReader import *
from ..TurbulenceParameters.DataAggregator import *


class DownloaderTest(unittest.TestCase):
    
    def test_download(self):
        '''Testing download from a remote server'''
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        self.assertGreater(len(downloader.binary_data), 0)

class ParserTest(unittest.TestCase):
    
    def setUp(self):
        self.downloader = DataDownloader()
        self.downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        self.downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        self.downloader.download()

    def test_parse(self):
        '''Testing conversion of binary files to numpy array'''
        parser = BytesParser()
        data = parser.parse(self.downloader.binary_data[0])
        for binary_file in self.downloader.binary_data[1:]:
            data = np.append(data, parser.parse(binary_file), axis=1)
        self.assertEqual(data.shape[0], 7)
        os.remove('TurbulenceParameters/Data/temporary_file.19B')

class WriterTest(unittest.TestCase):

    def setUp(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        parser = BytesParser()
        self.data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            self.data = np.append(self.data, parser.parse(binary_file), axis=1)


    def test_write(self):
        '''Testing file writing to PC memory'''
        writer = CsvWriter()
        writer.save_csv(self.data, 'test_file')
        self.assertIn('test_file.csv', os.listdir(path="TurbulenceParameters/Data/"))
        os.remove('TurbulenceParameters/Data/test_file.csv')
        os.remove('TurbulenceParameters/Data/temporary_file.19B')

class ReaderTest(unittest.TestCase):

    def setUp(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        parser = BytesParser()
        data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            data = np.append(data, parser.parse(binary_file), axis=1)
        writer = CsvWriter()
        writer.save_csv(data, 'test_file')


    def test_read(self):
        '''Testing reading files from PC memory'''
        reader = CsvReader()
        self.assertEqual(reader.read('test_file.csv').shape[0], 7)
        os.remove('TurbulenceParameters/Data/test_file.csv')
        os.remove('TurbulenceParameters/Data/temporary_file.19B')






class AggregatorTest(unittest.TestCase):

    def setUp(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        parser = BytesParser()
        self.data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            self.data = np.append(self.data, parser.parse(binary_file), axis=1)

    def test_aggregate(self):
        '''Testing data reduction by averaging'''
        aggregator = DataAggregator()
        aggregated_data = aggregator.aggregate(self.data)
        self.assertEqual(aggregated_data.shape[1], self.data.shape[1]//100)
        os.remove('TurbulenceParameters/Data/temporary_file.19B')

class CalculatorTest(unittest.TestCase):

    def setUp(self):
        downloader = DataDownloader()
        downloader.start_datetime = datetime.strptime('15.08.2018 15:00', '%d.%m.%Y %H:%M')
        downloader.end_datetime = datetime.strptime('15.08.2018 16:00', '%d.%m.%Y %H:%M')
        downloader.download()
        parser = BytesParser()
        self.data = parser.parse(downloader.binary_data[0])
        for binary_file in downloader.binary_data[1:]:
            self.data = np.append(self.data, parser.parse(binary_file), axis=1)

    def test_calculate(self):
        '''Testing a function to calculate turbulence parameters'''
        calculator = ParametersCalculator()
        self.assertGreater(len(calculator.calculate(self.data)), 0)
        os.remove('TurbulenceParameters/Data/temporary_file.19B')

class CommonTest(unittest.TestCase):
    
    def test_all(self):
        '''Test a full cycle of user actions'''
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
        self.assertEqual(aggregated_data.shape[1], data.shape[1] // 100)

        calculator = ParametersCalculator()
        calculator.calculate(aggregated_data)
        self.assertGreater(len(calculator.calculate(data)), 0)

        writer = CsvWriter()
        writer.save_csv(aggregated_data, 'test_file')
        self.assertIn('test_file.csv', os.listdir(path='TurbulenceParameters/Data/'))

        reader_tmp = CsvReader()
        self.assertEqual(reader_tmp.read('test_file.csv').shape[0], 7)

        os.remove('TurbulenceParameters/Data/test_file.csv')
        os.remove('TurbulenceParameters/Data/temporary_file.19B')

if __name__ == "__main__":
    unittest.main()
