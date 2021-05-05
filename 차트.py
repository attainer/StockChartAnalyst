import sys
sys.path.append('./model')
sys.path.append('./view')
sys.path.append('./controller')

from PyQt5.QtWidgets import *

from chartModel import ChartModel
from chartView import ChartView
from chartController import ChartController

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.model = ChartModel()
        self.controller = ChartController(self.model)
        self.view = ChartView(self.model, self.controller)
        self.view.show()

if __name__ == "__main__":
    app = App(sys.argv)
    app.exec_()