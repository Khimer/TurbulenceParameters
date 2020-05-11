import csv
import numpy as np


class CsvReader():
    def __init__(self):
        pass

    def read(self, name):
        with open('TurbulenceParameters/Data/' + name, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            for raw in range(1, len(data)):
                data[raw] = [float(x) for x in data[raw]]
            data = np.array(data[1:]).T
            return data


if __name__ == "__main__":
    reader = CsvReader()
    a = reader.read('babaka')
