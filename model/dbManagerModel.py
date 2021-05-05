from PyQt5.QtCore import *

class DBManagerModel(QObject):
    
    infoListChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self._infoList = []
    @property
    def infoList(self):
        return self._infoList

    @infoList.setter
    def infoList(self, value):
        self._infoList = value
        self.infoListChanged.emit(value)