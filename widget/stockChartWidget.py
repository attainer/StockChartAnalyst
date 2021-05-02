import pyqtgraph as pg
from PyQt5.QtWidgets import *

from chartWidget import ChartWidget
from candlestickItem import CandlestickItem
from barchartItem import BarchartItem

class StockChartWidget(ChartWidget):
    def getPercent(self, before, after):
        delta = after - before
        percent = delta / float(before) * 100

        return round(percent, 2)

    def getTooltipText(self, x, y):

        x = int(round(x))
        y = int(round(y))

        if x < 0:
            return

        if len(self.data) > x:
            prevPrice = 0
            data = self.data[x]

            if x >= 1:
                prevPrice = self.data[x -1]['close']
            else:
                prevPrice = self.data[0]['open']

            openPP = self.getPercent(prevPrice, data['open'])
            highPP = self.getPercent(prevPrice, data['high'])
            lowPP = self.getPercent(prevPrice, data['low'])
            closePP = self.getPercent(prevPrice, data['close'])

            time = str(data['time'])
            if self.type == 'D' or self.type == 'M' or self.type == 'W':
                time = str(data['date'])

            openText = "시가: %d (%.2f%%)" % (data['open'], openPP)
            highText = "고가: %d (%.2f%%)" % (data['high'], highPP)
            lowText = "저가: %d (%.2f%%)" % (data['low'], lowPP)
            closeText = "종가: %d (%.2f%%)" % (data['close'], closePP)

            text = (
                "시간: " + time
                + "\n" + openText
                + "\n" + highText
                + "\n" + lowText
                + "\n" + closeText
                + "\n" + "거래량: " + str(data['volume'])
                + "\n" + "가격: " + str(y)
                )


            if data['sell'] > 0:
                text += "\n" + "체결강도: " + str(round(data['buy'] / data['sell'] * 100))

            if self.isDrag == True and self.mode == 'calc':
                text += "\n차이: %.2f%%" % self.currentPercent

            return text

    def getAveLine(self, datas, n):
        aveList = []
        for i in range(len(datas) - n + 1):
            data = datas[i:i+n]

            ave = sum(data) / float(len(data))
            aveList.append(ave)

        return aveList

    def addTmpLine(self, price):
        tmp = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen(color=(255, 0, 0, 255)))
        tmp.setPos(price)
        self.tmpLine.append(tmp)
        self.plot.addItem(tmp)

    def updateData(self, data, type, targetDate):
        for i in self.tmpLine:
            self.plot.removeItem(i)

        self.tmpLine = []

        self.data = data
        self.type = type
        self.candleChart.set_data(data, targetDate)

        chartData = {
            'volume' : [],
            'buyAndSell' : [],
            'sell' : [],
            'close' : [],
        }

        IsBuyAndSellExist = False
        ticks = []

        if self.type == 'D' or self.type == 'M' or self.type == 'W':
            for i in range(len(data)):
                if i % 20 == 0:
                    ticks.append([i, data[i]['date']])
                chartData['volume'].append(data[i]['volume'])
                chartData['close'].append(data[i]['close'])

        for i in range(len(data)):
            if 'buy' in data[i] and 'sell' in data[i]:
                IsBuyAndSellExist = True
                chartData['buyAndSell'].append(data[i]['buy'] + data[i]['sell'])
                chartData['sell'].append(data[i]['sell'])
            else:
                chartData['buyAndSell'].append(0)
                chartData['sell'].append(0)
            chartData['close'].append(data[i]['close'])

        ax = self.plot2.getAxis('bottom')
        ax.setTicks([ticks])

        self.ticks = ticks

        if IsBuyAndSellExist == False:
            self.volumeRed.set_data(chartData['volume'])
        else:
            self.volumeGreen.set_data(chartData['volume'])
            self.volumeRed.set_data(chartData['buyAndSell'])
            self.volumeBlue.set_data(chartData['sell'])

        m5 = self.getAveLine(chartData['close'], 5)
        m10 = self.getAveLine(chartData['close'], 10)
        m20 = self.getAveLine(chartData['close'], 20)
        m60 = self.getAveLine(chartData['close'], 60)
        m120 = self.getAveLine(chartData['close'], 120)

        self.grayAveLine.setData(x=list(range(5 - 1, len(chartData['close']))), y=m5)
        self.redAveLine.setData(x=list(range(10 - 1, len(chartData['close']))), y=m10)
        self.orangeAveLine.setData(x=list(range(20 - 1, len(chartData['close']))), y=m20)
        self.greenAveLine.setData(x=list(range(60 - 1, len(chartData['close']))), y=m60)
        self.blueAveLine.setData(x=list(range(120 - 1, len(chartData['close']))), y=m120)

        self.updateRange(0, len(data))

        self.slider.setMaximum(len(self.data))
        self.slider.setValue(0)
        for i in self.tmpLine:
            self.plot.addItem(i)

    def __init__(self, parent=None, **kargs):
        ChartWidget.__init__(self, parent, **kargs)

        self.plotCandle = self.plot
        self.plotBar = self.plot2

        self.candleChart = CandlestickItem([])
        self.plot.addItem(self.candleChart)
        self.data = []

        self.volumeGreen = BarchartItem([], (0, 255, 0))
        self.volumeRed = BarchartItem([], (255, 0, 0))
        self.volumeBlue = BarchartItem([], (0, 0, 255))

        self.plot2.addItem(self.volumeGreen)
        self.plot2.addItem(self.volumeRed)
        self.plot2.addItem(self.volumeBlue)

        self.grayAveLine = self.plot.plot([], [], pen=pg.mkPen(color=(100, 100, 100, 127)))
        self.redAveLine = self.plot.plot([], [], pen=pg.mkPen(color=(255, 0, 0, 127)))
        self.orangeAveLine = self.plot.plot([], [], pen=pg.mkPen(color=(255, 127, 0, 127), width=2))
        self.greenAveLine = self.plot.plot([], [], pen=pg.mkPen(color=(0, 255, 0, 127)))
        self.blueAveLine = self.plot.plot([], [], pen=pg.mkPen(color=(0, 0, 255, 127)))


        self.tmpLine = []