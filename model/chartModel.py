from PyQt5.QtCore import *

class ChartModel(QObject):

    dataChanged = pyqtSignal(list)
    chartDataChanged = pyqtSignal(list)
    currentIndexChanged = pyqtSignal(int)
    codeChanged = pyqtSignal(str)
    dateChanged = pyqtSignal(str)
    companyNameChanged = pyqtSignal(str)
    marketCapChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self._data = []
        self._chartData = []
        self._currentIndex = 1
        self._code = ""
        self._date = ""
        self._companyName = ""
        self._marketCap = 0
        self.chartType = 'D'
        self.period = 1
        self.prevDayCnt = 10
        self.nextDayCnt = 0
        self.prevMinCnt = 0
        self.nextMinCnt = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.dataChanged.emit(value)

    @property
    def chartData(self):
        return self._chartData

    @chartData.setter
    def chartData(self, value):
        self._chartData = value
        self.chartDataChanged.emit(value)

    @property
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, value):
        self._currentIndex = value
        self.currentIndexChanged.emit(value)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value
        self.codeChanged.emit(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.dateChanged.emit(value)

    @property
    def companyName(self):
        return self._companyName

    @companyName.setter
    def companyName(self, value):
        self._companyName = value
        self.companyNameChanged.emit(value)

    @property
    def marketCap(self):
        return self._marketCap

    @marketCap.setter
    def marketCap(self, value):
        self._marketCap = value
        self.marketCapChanged.emit(value)

