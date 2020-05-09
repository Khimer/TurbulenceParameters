__author__ = "Rostislav Kolobov"
__version__ = "$Revision: 1.0 $"

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from TurbulenceParameters.MainWindow import *

app = QApplication(sys.argv)


class MainWindowTest(unittest.TestCase):
    '''Test the margarita mixer GUI'''

    def setUp(self):
        '''Create the GUI'''
        self.form = MainWindow()

    def setFormToDesiredValue(self):
        self.form.ui.lineEdit_3.setText('100')
        self.form.ui.lineEdit.setText('01:00')
        self.form.ui.lineEdit_2.setText('01:35')
        self.form.ui.lineEdit_5.setText('0.0255')
        self.form.ui.lineEdit_4.setText('375')
        self.form.ui.lineEdit_6.setText('1.574')
        self.form.ui.lineEdit_7.setText('1.222')
        self.form.ui.calendarWidget.setSelectedDate(datetime(2018, 1, 1))

    def test_defaults(self):
        ''' Test the GUI in its default state '''
        self.assertEqual(self.form.ui.lineEdit_3.text(), '10')
        self.assertEqual(self.form.ui.lineEdit.text(), '00:00')
        self.assertEqual(self.form.ui.lineEdit_2.text(), '00:10')
        self.assertEqual(self.form.ui.lineEdit_5.text(), '0.0125')
        self.assertEqual(self.form.ui.lineEdit_4.text(), '331')
        self.assertEqual(self.form.ui.lineEdit_6.text(), '1.225')
        self.assertEqual(self.form.ui.lineEdit_7.text(), '1')
        self.assertEqual(self.form.ui.label_5.text(), 'Здесь появится указанный диапазон')
        self.assertEqual(self.form.ui.label_20.text(), '')
        self.assertEqual(self.form.ui.label_21.text(), '')
        self.assertEqual(self.form.ui.label_3.text(), '')
        self.assertEqual(self.form.ui.label_4.text(), '')
        self.assertEqual(self.form.ui.label_9.text(), '')
        self.assertEqual(self.form.ui.label_22.text(), '')

    def test_full_cycle(self):
        '''Test the GUI in a full cycle of user actions'''
        self.setFormToDesiredValue()
        QTest.mouseClick(self.form.ui.pushButton, Qt.LeftButton)
        self.assertEqual(self.form.ui.label_3.text(), '01.01.2018 01:00')
        QTest.mouseClick(self.form.ui.pushButton_2, Qt.LeftButton)
        self.assertEqual(self.form.ui.label_4.text(), '01.01.2018 01:35')
        QTest.mouseClick(self.form.ui.pushButton_3, Qt.LeftButton)
        self.assertEqual(self.form.ui.label_5.text(), '01.01.2018 01:00 - 01.01.2018 01:35')
        if self.form.service.connection:
            QTest.mouseClick(self.form.ui.pushButton_4, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_8.text(), 'Загрузка завершена')
            QTest.mouseClick(self.form.ui.pushButton_7, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_20.text(), 'Усреднение завершено!')
            QTest.mouseClick(self.form.ui.pushButton_8, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_21.text(), 'Данные сохранены!')
            QTest.mouseClick(self.form.ui.pushButton_9, Qt.LeftButton)
            self.assertGreater(float(self.form.ui.tableWidget.item(1, 0).text()), 0)
            QTest.mouseClick(self.form.ui.pushButton_10, Qt.LeftButton)
            self.assertEqual(self.form.ui.comboBox.currentText(), '01.01.2018 01.00-01.01.2018 01.35.csv')
            self.form.ui.comboBox.setCurrentIndex(0)
            QTest.mouseClick(self.form.ui.pushButton_5, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_9.text(), 'Загрузка завершена!')
        else:
            QTest.mouseClick(self.form.ui.pushButton_4, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_8.text(), 'ОШИБКА! Отсутствует подключение к серверу '
                                                          'или неправильно указан диапазон')
            QTest.mouseClick(self.form.ui.pushButton_7, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_20.text(), 'Нет данных для усреднения или неверно указан n!')
            QTest.mouseClick(self.form.ui.pushButton_8, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_21.text(), 'Нет данных для сохранения!')
            QTest.mouseClick(self.form.ui.pushButton_9, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_22.text(), 'Нет данных для расчета!')
            QTest.mouseClick(self.form.ui.pushButton_5, Qt.LeftButton)
            self.assertEqual(self.form.ui.label_9.text(), 'Файл не выбран!')


if __name__ == "__main__":
    unittest.main()
