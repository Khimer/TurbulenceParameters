import csv


class CsvWriter():
    def __init__(self):
        pass

    def save_csv(self, data, name):
        name_col = ["temperature", "south_component", "east_component", "vertical_component",
                    "pressure", "relative_humidity", "error_sign"]
        with open(name+'.csv', "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(name_col)
            writer.writerows(data.T)
        print("Сохранено в файл")