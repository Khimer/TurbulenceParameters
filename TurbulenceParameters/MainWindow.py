from TurbulenceParameters.MainWindowQt import Ui_MainWindow
from TurbulenceParameters.Service import *
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


#  pyuic5 L:/Program/PyStorm/TurbulenceParameters/TurbulenceParameters/MainWindowQt.ui -o L:/Program/PyStorm/TurbulenceParameters/TurbulenceParameters/MainWindowQt.py

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.service = Service()
        self.download_permission_flag = 0
        self.service.check_connection_and_time_range()
        if self.service.connection:
            self.ui.label_19.setText('СЕРВЕР ДОСТУПЕН')
            self.ui.calendarWidget.setDateRange(self.service.availableTimeStart, self.service.availableTimeEnd)
        else:
            self.ui.label_5.setWordWrap(True)
            self.ui.label_19.setText('ПОДКЛЮЧЕНИЕ К СЕРВЕРУ ОТСУТСТВУЕТ')
        self.ui.lineEdit.setMaxLength(5)
        self.ui.lineEdit_2.setMaxLength(5)
        self.ui.pushButton.clicked.connect(self.set_start_of_range)
        self.ui.pushButton_2.clicked.connect(self.set_end_of_range)
        self.ui.pushButton_3.clicked.connect(self.submit_range)
        self.ui.pushButton_4.clicked.connect(self.download)
        self.ui.pushButton_5.clicked.connect(self.read)
        self.ui.pushButton_7.clicked.connect(self.aggregate)
        self.ui.pushButton_8.clicked.connect(self.write)
        self.ui.pushButton_9.clicked.connect(self.calculate)
        self.ui.pushButton_10.clicked.connect(self.update_list_files)
        # self.name_col = ["Температура","Южный компонент", "Восточный компонент", "Вертикальный компонент",
        #                      "Давление", "Относительная влажность", "Знак ошибки", "Высота измерений",
        #                      "Тип подстилающей поверхности"]

    def set_start_of_range(self):
        self.ui.label_3.setText(self.ui.calendarWidget.selectedDate().toString("dd.MM.yyyy")
                                + " " + self.ui.lineEdit.text())

    def set_end_of_range(self):
        self.ui.label_4.setText(self.ui.calendarWidget.selectedDate().toString("dd.MM.yyyy")
                                + " " + self.ui.lineEdit_2.text())

    def submit_range(self):
        def check_text(text):
            try:
                return (0 <= int(text[-5:-3]) <= 23) and (0 <= int(text[-2:]) <= 59) and (text[-3] == ':')
            except ValueError:
                return 0
            except IndexError:
                return 0

        if check_text(self.ui.label_3.text()) and check_text(self.ui.label_4.text()):
            start_time = datetime.strptime(self.ui.label_3.text(), '%d.%m.%Y %H:%M')
            end_time = datetime.strptime(self.ui.label_4.text(), '%d.%m.%Y %H:%M')
            if end_time > start_time:
                self.service.set_time_range([start_time, end_time])
                self.ui.label_5.setText(self.ui.label_3.text() + ' - ' + self.ui.label_4.text())
                self.download_permission_flag = 1
            else:
                self.ui.label_5.setWordWrap(True)
                self.ui.label_5.setText('ОШИБКА! ДАТА НАЧАЛА ИЗМЕРЕНИЙ БОЛЬШЕ ДАТЫ ОКОНЧАНИЯ!')
                self.download_permission_flag = 0
        else:
            self.ui.label_5.setWordWrap(True)
            self.ui.label_5.setText('ОШИБКА! ПЕРИОД ИЗМЕРЕНИЙ УКАЗАН НЕ ВЕРНО!')
            self.download_permission_flag = 0

    def download(self):
        self.ui.label_8.setWordWrap(True)
        if self.service.connection and self.download_permission_flag:
            self.service.data = np.array([])
            self.ui.label_8.setText('Загрузка данных...')
            self.service.download_data()
            self.ui.label_8.setText('Загрузка завершена')
        else:
            self.ui.label_8.setWordWrap(True)
            self.ui.label_8.setText('ОШИБКА! Отсутствует подключение к серверу или неправильно указан диапазон')

    def aggregate(self):
        if self.service.data.shape[0] != 0 and int(self.ui.lineEdit_3.text()):
            self.service.aggregator.amountAggregatedData = int(self.ui.lineEdit_3.text())
            self.service.aggregate_data()
            self.ui.label_20.setStyleSheet("color: rgb(0, 0, 0);")
            self.ui.label_20.setText('Усреднение завершено!')
        else:
            self.ui.label_20.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_20.setText('Нет данных для усреднения или неверно указан n!')

    def write(self):
        if self.service.data.shape[0] != 0:
            self.service.save_data([self.ui.label_3.text(), self.ui.label_4.text()])
            self.ui.label_21.setStyleSheet("color: rgb(0, 0, 0);")
            self.ui.label_21.setText('Данные сохранены!')
        else:
            self.ui.label_21.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_21.setText('Нет данных для сохранения!')

    def calculate(self):
        try:
            if self.service.data.shape[0] != 0:
                self.service.calculator.constants = [float(self.ui.lineEdit_5.text()), float(self.ui.lineEdit_4.text()),
                                                     float(self.ui.lineEdit_6.text()), float(self.ui.lineEdit_7.text())]
                row = 0
                for parameter in self.service.calculate_turbulence_parameters():
                    cellinfo = QTableWidgetItem(str(round(parameter, 5)))
                    self.ui.tableWidget.setItem(row, 0, cellinfo)
                    row += 1
                self.ui.label_23.clear()
            else:
                self.ui.label_22.setStyleSheet("color: rgb(255, 0, 0);")
                self.ui.label_22.setText('Нет данных для расчета!')
        except ValueError:
            self.ui.label_23.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_23.setText('ПЕРЕМЕННЫЕ УКАЗАНЫ НЕКОРРЕКТНО!')

    def update_list_files(self):
        self.ui.comboBox.clear()
        for file in self.service.get_list_files():
            self.ui.comboBox.addItem(file)
        self.ui.comboBox.setCurrentIndex(0)

    def read(self):
        if self.ui.comboBox.currentText():
            self.service.data = np.array([])
            self.service.read_data(self.ui.comboBox.currentText())
            self.ui.label_9.setText('Загрузка завершена!')
        else:
            self.ui.label_9.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_9.setText('Файл не выбран!')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
