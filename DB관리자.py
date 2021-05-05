import sys
sys.path.append('./model')
sys.path.append('./view')
sys.path.append('./controller')

from PyQt5.QtWidgets import *

from dbManagerModel import DBManagerModel
from dbManagerView import DBManagerView
from dbManagerController import DBManagerController

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.model = DBManagerModel()
        self.view = DBManagerView(self.model)
        self.controller = DBManagerController(self.model)
        self.view.show()

if __name__ == "__main__":
    app = App(sys.argv)
    app.exec_()