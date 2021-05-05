import sys
sys.path.append('./lib')

from PyQt5.QtCore import *

from stockDB import StockDB

class DBManagerController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.db = StockDB()
        self.model.infoList = list(self.db.info.find())