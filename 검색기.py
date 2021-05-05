import sys
sys.path.append('./model')
sys.path.append('./view')
sys.path.append('./controller')

from PyQt5.QtWidgets import *

from searcherModel import SearcherModel
from searcherView import SearcherView
from searcherController import SearcherController

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.model = SearcherModel()
        self.controller = SearcherController(self.model)
        self.view = SearcherView(self.model, self.controller)
        self.view.show()

if __name__ == "__main__":
    app = App(sys.argv)
    app.exec_()