from PyQt5.QtCore import *

class SearcherModel(QObject):
    
    conditionChanged = pyqtSignal(str)
    dayFromChanged = pyqtSignal(str)
    dayToChanged = pyqtSignal(str)
    isModifiedChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self._condition = ""
        self._dayFrom = 0
        self._dayTo = 0
        self._isModified = False

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels);

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, value):
        self._condition = value
        self.conditionChanged.emit(value)

    @property
    def dayFrom(self):
        return self._dayFrom

    @dayFrom.setter
    def dayFrom(self, value):
        self._dayFrom = value
        self.dayFromChanged.emit(value)

    @property
    def dayTo(self):
        return self._dayTo

    @dayTo.setter
    def dayTo(self, value):
        self._dayTo = value
        self.dayToChanged.emit(value)

    @property
    def isModified(self):
        return self._isModified

    @isModified.setter
    def isModified(self, value):
        self._isModified = value
        self.isModifiedChanged.emit(value)