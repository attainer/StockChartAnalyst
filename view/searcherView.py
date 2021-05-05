from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import ctypes
import subprocess

CP_console = "cp" + str(ctypes.cdll.kernel32.GetConsoleOutputCP())
form_class = uic.loadUiType("ui/검색기.ui")[0]

class SearcherView(QMainWindow, form_class):
    def __init__(self, model, controller):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.controller = controller

        self.model.process.readyRead.connect(self.dataReady)

        self.textCondition.textChanged.connect(lambda: self.controller.changeCondition(self.textCondition.toPlainText()))
        self.lineDayFrom.textEdited.connect(self.controller.changeDayFrom)
        self.lineDayTo.textEdited.connect(self.controller.changeDayTo)
        self.checkModified.stateChanged.connect(self.controller.changeModified)

        self.model.conditionChanged.connect(self.onConditionChanged)
        self.model.dayFromChanged.connect(self.onDayFromChanged)
        self.model.dayToChanged.connect(self.onDayToChanged)
        self.model.isModifiedChanged.connect(self.onIsModifiedChanged)

        self.buttonOpenCondition.clicked.connect(self.openCondition)
        self.buttonSaveCondition.clicked.connect(self.saveCondition)
        self.buttonOpenChart.clicked.connect(self.openChart)
        self.buttonRunCondition.clicked.connect(self.controller.runCondition)

    @pyqtSlot(str)
    def onConditionChanged(self, value):
        if self.textCondition.toPlainText() != value:
            self.textCondition.setText(value)

    @pyqtSlot(str)
    def onDayFromChanged(self, value):
        self.lineDayFrom.setText(value)

    @pyqtSlot(str)
    def onDayToChanged(self, value):
        self.lineDayTo.setText(value)

    @pyqtSlot(bool)
    def onIsModifiedChanged(self, value):
        if value:
            self.checkModified.setChecked(True)
        else:
            self.checkModified.setChecked(False)

    @pyqtSlot()
    def openCondition(self):
        fileName = QFileDialog.getOpenFileName(
               self, 'Open File', '', 'text (*.txt)')
        self.controller.openCondition(fileName)

    @pyqtSlot()
    def saveCondition(self):
        fileName = QFileDialog.getSaveFileName(
               self, 'Save File', '', 'text (*.txt)')
        self.controller.saveCondition(fileName)

    @pyqtSlot()
    def openChart(self):
        subprocess.Popen('python 차트.py', shell=True)

    @pyqtSlot()
    def dataReady(self):
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(cursor.End)

        string = self.model.process.readAll().data().decode(CP_console)
        cursor.insertText(string)
        self.plainTextEdit.ensureCursorVisible()