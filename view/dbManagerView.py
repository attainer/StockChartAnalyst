from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/DB관리자.ui")[0]

class DBManagerView(QMainWindow, form_class):
    def __init__(self, model):
        super().__init__()
        self.setupUi(self)
        
        self.model = model
        self.model.infoListChanged.connect(self.UpdateTable)

    def UpdateTable(self, infoList):
        row = self.tableStockInfo.rowCount()
        if row < len(infoList):
            self.tableStockInfo.insertRow(len(infoList) - row)

        for i in range(len(infoList)):
            info = infoList[i]

            row = self.tableStockInfo.rowCount()
            if row < len(infoList):
                self.tableStockInfo.insertRow(row)

            self.tableStockInfo.setItem(i, 0, QTableWidgetItem(info['name']))
            self.tableStockInfo.setItem(i, 1, QTableWidgetItem(str(info['lastFrom'])))
            self.tableStockInfo.setItem(i, 2, QTableWidgetItem(str(info['lastTo'])))