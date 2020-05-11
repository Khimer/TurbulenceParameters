import numpy as np
import os
import time


class BytesParser():
    def __init__(self):
        pass

    def parse(self, binary_file):
        with open('TurbulenceParameters/Data/temporary_file.19B', 'wb') as file:  # Запись бинарных данных в файл
            file.write(binary_file)
        end_data_place = os.path.getsize('TurbulenceParameters/Data/temporary_file.19B') - 14  # Конец расположения данных в файле
        number_of_measurements = (end_data_place - 17) // 13
        tmp_data = np.ones((7, number_of_measurements))
        with open('TurbulenceParameters/Data/temporary_file.19B', 'rb') as binary:
            #print("Файл открыт")
            year_start = int.from_bytes(binary.read(2), byteorder='little')
            if year_start <= int(time.strftime("%Y", time.localtime())):
                month_start = int.from_bytes(binary.read(2), byteorder='little')
                day_start = int.from_bytes(binary.read(2), byteorder='little')
                hour_start = int.from_bytes(binary.read(2), byteorder='little')
                minute_start = int.from_bytes(binary.read(2), byteorder='little')
                second_start = int.from_bytes(binary.read(2), byteorder='little')
                millisecond_start = int.from_bytes(binary.read(2), byteorder='little')
                Zu = int.from_bytes(binary.read(2), byteorder='little')  # Высота измерений
                p = int.from_bytes(binary.read(1), byteorder='little')  # Номер типа подстилающей поверхности
                measurement_number = 0
                while measurement_number < number_of_measurements:
                    tmp_data[0][measurement_number] = (int.from_bytes(binary.read(2), byteorder='little',
                                                                  signed=True)) / 100
                    tmp_data[1][measurement_number] = (int.from_bytes(binary.read(2), byteorder='little',
                                                                  signed=True)) / 100
                    tmp_data[2][measurement_number] = (int.from_bytes(binary.read(2), byteorder='little',
                                                                  signed=True)) / 100
                    tmp_data[3][measurement_number] = (
                                                      int.from_bytes(binary.read(2), byteorder='little',
                                                                     signed=True)) / 100
                    tmp_data[4][measurement_number] = (int.from_bytes(binary.read(2), byteorder='little')) / 10
                    tmp_data[5][measurement_number] = (int.from_bytes(binary.read(2), byteorder='little')) / 100
                    tmp_data[6][measurement_number] = (int.from_bytes(binary.read(1), byteorder='little'))
                    measurement_number += 1
                binary.seek(-14, 2)
                year_end = int.from_bytes(binary.read(2), byteorder='little')
                month_end = int.from_bytes(binary.read(2), byteorder='little')
                day_end = int.from_bytes(binary.read(2), byteorder='little')
                hour_end = int.from_bytes(binary.read(2), byteorder='little')
                minute_end = int.from_bytes(binary.read(2), byteorder='little')
                second_end = int.from_bytes(binary.read(2), byteorder='little')
                millisecond_end = int.from_bytes(binary.read(2), byteorder='little')
                #print(tmp_data)
                return tmp_data
            else:
                print("Файл неисправен")
