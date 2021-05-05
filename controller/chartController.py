import sys
sys.path.append('./widget')
sys.path.append('./lib')

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import *

from stockChart import StockChart
from stockDB import StockDB
from datetime import datetime, timedelta

class ChartController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.db = StockDB()
        self.chart = StockChart(self.db)

    def changePrevDayCnt(self, value):
        self.model.prevDayCnt = int(value)
        self.updateChart(self.model.code, self.model.date)

    def changeNextDayCnt(self, value):
        self.model.nextDayCnt = int(value)
        self.updateChart(self.model.code, self.model.date)

    def changePrevMinCnt(self, value):
        self.model.prevMinCnt = int(value)
        self.updateChart(self.model.code, self.model.date)

    def changeNextMinCnt(self, value):
        self.model.nextMinCnt = int(value)
        self.updateChart(self.model.code, self.model.date)

    def changeFileIndex(self, value):
        self.model.currentIndex = int(value)
        self.updateChartFromFile(self.model.currentIndex)


    def downloadFile(self, fileName):
        if fileName[0] != "":
            data = []
            f = open(fileName[0], 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split(' ')
                if len(line) < 2:
                    break
                data.append((line[0], line[1].strip()))
            f.close()

            self.model.data = data
            self.updateChartFromFile(0)

    def updateChartFromFile(self, index):
        if len(self.model.data) > index:
            self.model.code = self.model.data[index][0]
            self.model.date = self.model.data[index][1]
            self.model.currentIndex = index + 1
            self.updateChart(self.model.code, self.model.date)

    def getPrev(self):
        current = self.model.currentIndex
        prev = current - 1
        if prev >= 1:
            self.updateChartFromFile(prev - 1)

    def getNext(self):
        current = self.model.currentIndex
        next = current + 1
        if next <= len(self.model.data):
            self.updateChartFromFile(next - 1)

    def updateChart(self, code, date):
        prev = 0
        next = 0
        chartType = self.model.chartType

        if chartType == 'D' or chartType == 'M' or chartType == 'W':
            prev = self.model.prevDayCnt
            next = self.model.nextDayCnt
        else:
            prev = self.model.prevMinCnt
            next = self.model.nextMinCnt

        targetDate = datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))
        prevDate = (targetDate - timedelta(days=prev * 2 + 2)).strftime('%Y%m%d')
        nextDate = (targetDate + timedelta(days=next * 2 + 2)).strftime('%Y%m%d')

        if chartType == 'D':
            chartData = self.chart.getDayChart(code, int(prevDate), int(nextDate))
        else:
            chartData = self.chart.getMinChart(code, int(prevDate), int(nextDate), self.model.period)

        if chartType == 'D' and self.model.period == 7:
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

            self.model.chartData = chartData

            info = self.db.info.find_one({"code" : code});
            self.model.companyName = info['name']

            if 'cap' in chartData[-1]:
                self.model.marketCap = chartData[-1]['cap']

    def changePeriod(self, period):
        if period == 'D':
            self.model.chartType = 'D'
            self.model.period = 1
        elif period == 'W':
            self.model.chartType = 'D'
            self.model.period = 7
        elif period == 'M':
            self.model.chartType = 'D'
            self.model.period = 1
        else:
            self.model.chartType = 'm'
            self.model.period = period
        self.updateChart(self.model.code, self.model.date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()