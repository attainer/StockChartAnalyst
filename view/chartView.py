import sys
sys.path.append('./widget')

import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5 import *

from stockChartWidget import StockChartWidget

form_class = uic.loadUiType("ui/차트.ui")[0]

class ChartView(QMainWindow, form_class):
    def __init__(self, model, controller):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.controller = controller

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

        self.inputPrevDayCnt.textEdited.connect(self.controller.changePrevDayCnt)
        self.inputNextDayCnt.textEdited.connect(self.controller.changeNextDayCnt)
        self.inputPrevMinCnt.textEdited.connect(self.controller.changePrevMinCnt)
        self.inputNextMinCnt.textEdited.connect(self.controller.changeNextMinCnt)
        self.inputFileIndex.textEdited.connect(self.controller.changeFileIndex)

        self.model.dataChanged.connect(self.onDataChanged)
        self.model.chartDataChanged.connect(self.onChartDataChanged)
        self.model.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.model.codeChanged.connect(self.onCodeChanged)
        self.model.dateChanged.connect(self.onDateChanged)
        self.model.companyNameChanged.connect(self.onCompanyNameChanged)
        self.model.marketCapChanged.connect(self.onMarketCapChanged)

        self.button_file.clicked.connect(self.downloadFile)
        self.button_prev.clicked.connect(self.controller.getPrev)
        self.button_next.clicked.connect(self.controller.getNext)
        self.button_mode.clicked.connect(self.changeMode)
        self.button_15min.clicked.connect(lambda: self.controller.changePeriod(15))
        self.button_5min.clicked.connect(lambda: self.controller.changePeriod(5))
        self.button_1min.clicked.connect(lambda: self.controller.changePeriod(1))
        self.button_day.clicked.connect(lambda: self.controller.changePeriod('D'))
        self.button_week.clicked.connect(lambda: self.controller.changePeriod('W'))
        self.button_month.clicked.connect(lambda: self.controller.changePeriod('M'))

    def onDataChanged(self):
        self.labelFileLength.setText(str(len(self.model.data)))

    def onChartDataChanged(self):
        self.stockChartWidget.updateData(self.model.chartData, self.model.chartType, self.model.date)

    def onCurrentIndexChanged(self):
        self.inputFileIndex.setText(str(self.model.currentIndex))
        self.labelFileIndex.setText(str(self.model.currentIndex))

    def onCodeChanged(self):
        self.inputCode.setText(self.model.code)

    def onDateChanged(self):
        self.inputDate.setText(str(self.model.date))

    def onCompanyNameChanged(self):
        self.labelCompanyName.setText(self.model.companyName)

    def onMarketCapChanged(self):
        self.labelMarketCap.setText(str(round(self.model.marketCap / 100000000)) + '억')

    def downloadFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
               self, 'Open File', '', 'text (*.txt)')
        self.controller.downloadFile(fileName)

    def changeMode(self):
        if self.stockChartWidget.mode == 'calc':
            self.stockChartWidget.changeMode('zoom')
        else:
            self.stockChartWidget.changeMode('calc')