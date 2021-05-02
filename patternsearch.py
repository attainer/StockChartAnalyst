import sys
sys.path.append('./widget')
sys.path.append('./lib')

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import sys
import os
import ctypes
import subprocess
import pathlib

CP_console = "cp" + str(ctypes.cdll.kernel32.GetConsoleOutputCP())
form_class = uic.loadUiType("검색기.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels);
        self.process.readyRead.connect(self.dataReady)
        self.process.finished.connect(self.dataReady)

        self.buttonOpenCondition.clicked.connect(self.openCondition)
        self.buttonRunCondition.clicked.connect(self.runCondition)
        self.buttonSaveCondition.clicked.connect(self.saveCondition)
        self.buttonOpenChart.clicked.connect(self.openChart)

    def openCondition(self):
        fileName = QFileDialog.getOpenFileName(
               self, 'Open File', '', 'text (*.txt)')

        if fileName[0] != "":
            f = open(fileName[0], 'r')
            lines = f.readlines()
            f.close()

            if len(lines) < 2:
                return
            conditions = lines[0].split("|")
            if len(conditions) < 3:
                return

            self.lineDayFrom.setText(conditions[0])
            self.lineDayTo.setText(conditions[1])
            if int(conditions[2]) == 1:
                self.checkModified.setChecked(True)
            else:
                self.checkModified.setChecked(False)

            self.textCondition.setText("".join(lines[1:]))

    def saveCondition(self):
        fileName = QFileDialog.getSaveFileName(
               self, 'Save File', '', 'text (*.txt)')

        if fileName[0] != "":
            f = open(fileName[0], 'w')
            f.write(self.lineDayFrom.text() + "|" + self.lineDayTo.text() + "|" + str(int(self.checkModified.isChecked())) + "\n")
            f.write(self.textCondition.toPlainText())
            f.close()

    def runCondition(self):
        pycode = self.textCondition.toPlainText()
        appender = "\n        "
        pycode = pycode.split("\n")
        pycode = appender + appender.join(pycode)
        pathlib.Path("tmp").mkdir(exist_ok=True)
        f = open("tmp/tmp.py", 'w', encoding="utf-8")
        f.write("""
import os, sys
sys.path.append('widget')
sys.path.append('lib')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conditionManager import ConditionManager
from conditionManager import GameManager
class 전략(GameManager):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.fromDate = {}
        self.toDate = {}
        self.isModified = {}
    
    def Strategy(self, x):
        일봉 = self.일봉
        분봉 = self.분봉
        종목코드 = self.code
        상한가 = self.상한가
        저장 = self.addResult
        케이스발생 = self.addCase
{}

def Run(parameters):
    game = 전략(parameters)
    return game.Run()

if __name__ == '__main__':
    ConditionManager().Run(Run)
""".format(self.lineDayFrom.text(), self.lineDayTo.text(), str(self.checkModified.isChecked()), pycode))

        f.close()

        self.process.start('python',['tmp/tmp.py'])

    def openChart(self):
        subprocess.Popen('python uichart.py', shell=True)

    def dataReady(self):
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(cursor.End)

        string = self.process.readAll().data().decode(CP_console)
        cursor.insertText(string)
        self.plainTextEdit.ensureCursorVisible()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()

    app.exec_()