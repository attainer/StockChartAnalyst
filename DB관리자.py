import sys
sys.path.append('./widget')
sys.path.append('./lib')

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from stockDB import StockDB
import os
import ctypes

CP_console = "cp" + str(ctypes.cdll.kernel32.GetConsoleOutputCP())
form_class = uic.loadUiType("ui/DB관리자.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = StockDB()
        self.updateAllTable(list(self.db.info.find()))

    def updateAllTable(self, infoList):
        row = self.tableStockInfo.rowCount()
        if row < len(infoList):
            print(len(infoList) - row)
            self.tableStockInfo.insertRow(len(infoList) - row)

        for i in range(len(infoList)):
            info = infoList[i]

            row = self.tableStockInfo.rowCount()
            if row < len(infoList):
                self.tableStockInfo.insertRow(row)

            self.tableStockInfo.setItem(i, 0, QTableWidgetItem(info['name']))
            self.tableStockInfo.setItem(i, 1, QTableWidgetItem(str(info['lastFrom'])))
            self.tableStockInfo.setItem(i, 2, QTableWidgetItem(str(info['lastTo'])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()

    app.exec_()