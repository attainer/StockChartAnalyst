import sys
sys.path.append('./widget')
sys.path.append('./lib')

import pyqtgraph as pg
from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
from PyQt5 import *

from stockChartWidget import StockChartWidget
from stockChart import StockChart
from stockDB import StockDB
from datetime import datetime, timedelta

form_class = uic.loadUiType("ui/차트.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tooltip = QLabel(self)
        self.tooltip.setStyleSheet('background: white')
        self.tooltip.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Preferred)
        self.tooltip.setContentsMargins(0,0,0,0);
        self.tooltip.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.tooltip.hide()

        self.stockChartWidget.setTool(self.tooltip)
        self.stockChartWidget.setSlider(self.slider_horizon)
        
        self.uploaded = []

        self.db = StockDB()
        self.chart = StockChart(self.db)

        self.chartType = 'D'
        self.period = 1

        self.button_file.clicked.connect(self.uploadFile)
        self.button_prev.clicked.connect(self.getUploadedPrev)
        self.button_next.clicked.connect(self.getUploadedNext)
        self.button_mode.clicked.connect(self.changeMode)
        self.button_15min.clicked.connect(self.changePeriod15)
        self.button_5min.clicked.connect(self.changePeriod5)
        self.button_1min.clicked.connect(self.changePeriod1)
        self.button_day.clicked.connect(self.changePeriodDay)
        self.button_week.clicked.connect(self.changePeriodWeek)
        self.button_month.clicked.connect(self.changePeriodMonth)

    def uploadFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
               self, 'Open File', '', 'text (*.txt)')

        if fileName[0] != "":
            self.uploaded = []
            f = open(fileName[0], 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split(' ')
                if len(line) < 2:
                    break
                self.uploaded.append((line[0], line[1].strip()))
            f.close()

            self.label_file_length.setText(str(len(self.uploaded)))
            self.updateChartFromFile(0)

    def getUploadedPrev(self):
        current = int(self.input_file_index.toPlainText())
        prev = current - 1
        if prev >= 1:
            self.updateChartFromFile(prev - 1)

    def getUploadedNext(self):
        current = int(self.input_file_index.toPlainText())
        next = current + 1
        if next <= len(self.uploaded):
            self.updateChartFromFile(next - 1)

    def changeMode(self):
        if self.stockChartWidget.mode == 'calc':
            self.stockChartWidget.changeMode('zoom')
        else:
            self.stockChartWidget.changeMode('calc')

    def updateChartFromFile(self, index):
        if len(self.uploaded) > index:
            code = self.uploaded[index][0]
            date = self.uploaded[index][1]

            self.input_file_index.setText(str(index + 1))
            self.label_file_index.setText(str(index + 1))

            self.updateChart(code, date)

    def updateChartFromInput(self):
        code = self.input_code.toPlainText()
        date = self.input_date.toPlainText()

        self.updateChart(code, date)

    def updateChart(self, code, date):
        self.input_code.setText(code)
        self.input_date.setText(str(date))

        prev = 0
        next = 0

        if self.chartType == 'D' or self.chartType == 'M' or self.chartType == 'W':
            prev = self.input_prev_day_count.toPlainText()
            next = self.input_next_day_count.toPlainText()
        else:
            prev = self.input_prev_min_count.toPlainText()
            next = self.input_next_min_count.toPlainText()

        prev = int(prev)
        next = int(next)

        targetDate = datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))
        prevDate = (targetDate - timedelta(days=prev * 2 + 2)).strftime('%Y%m%d')
        nextDate = (targetDate + timedelta(days=next * 2 + 2)).strftime('%Y%m%d')

        if self.chartType == 'D':
            chartData = self.chart.getDayChart(code, int(prevDate), int(nextDate))
        else:
            chartData = self.chart.getMinChart(code, int(prevDate), int(nextDate), self.period)

        if self.chartType == 'D' and self.period == 7:
            chartData = self.chart.getCombinedDayToWeekChart(chartData)
        if len(chartData) != 0:

            dateList = set()
            for data in chartData:
                dateList.add(data['date'])
            dateList = list(dateList)
            dateList.sort()
            for i in range(len(dateList)):
                if str(dateList[i]) == date:
                    break

            prev = max(0, i - prev)
            next = i + next + 1

            for start in range(len(chartData)):
                if chartData[start]['date'] == dateList[prev]:
                    break

            if len(dateList) - 1 < next:
                end = len(chartData) + 1
            else:
                for end in range(start, len(chartData)):
                    if chartData[end]['date'] == dateList[next]:
                        break

            chartData = chartData[start:end]
            
            self.stockChartWidget.updateData(chartData, self.chartType, date)

            info = self.db.info.find_one({"code" : code});
            companyName = info['name']

            self.label_company_name.setText(companyName)
            if 'cap' in chartData[-1]:
                self.label_volume_total.setText(str(round(chartData[-1]['cap'] / 100000000)) + '억')

    def changePeriod(self, period):
        if period == 'D':
            self.chartType = 'D'
            self.period = 1
        elif period == 'W':
            self.chartType = 'D'
            self.period = 7
        elif period == 'M':
            self.chartType = 'M'
            self.period = 1
        else:
            self.chartType = 'm'
            self.period = period
        self.updateChartFromInput()

    def changePeriod15(self):
        self.changePeriod(3)

    def changePeriod5(self):
        self.changePeriod(5)

    def changePeriod1(self):
        self.changePeriod(1)

    def changePeriodDay(self):
        self.changePeriod('D')

    def changePeriodWeek(self):
        self.changePeriod('W')

    def changePeriodMonth(self):
        self.changePeriod('M')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()