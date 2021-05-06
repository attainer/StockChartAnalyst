from PyQt5.QtCore import *
import pathlib

class SearcherController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def changeCondition(self, value):
        self.model.condition = value

    def changeDayFrom(self, value):
        self.model.dayFrom = value

    def changeDayTo(self, value):
        self.model.dayTo = value

    def changeModified(self, value):
        self.model.isModified = value

    def openCondition(self, fileName):
        if fileName[0] != "":
            f = open(fileName[0], 'r')
            lines = f.readlines()
            f.close()

            if len(lines) < 2:
                return
            conditions = lines[0].split("|")
            if len(conditions) < 3:
                return

            self.model.dayFrom = conditions[0]
            self.model.dayTo = conditions[1]
            if int(conditions[2]) == 1:
                self.model.isModified = True
            else:
                self.model.isModified = False

            self.model.condition = "".join(lines[1:])

    def saveCondition(self, fileName):
        if fileName[0] != "":
            f = open(fileName[0], 'w')
            f.write(self.model.dayFrom + "|" + self.model.dayTo  + "|" + str(int(self.model.isModified)) + "\n")
            f.write(self.model.condition)
            f.close()

    def runCondition(self):
        pycode = self.model.condition
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
from gameManager import GameManager
from gameFunc import GameFunc
class 전략(GameManager):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.fromDate = {}
        self.toDate = {}
        self.isModified = {}
    
    def Strategy(self, x):
        일봉 = self.gameFunc.일봉
        분봉 = self.gameFunc.분봉
        종목코드 = self.code
        상한가 = self.gameFunc.상한가
        저장 = self.saveTmpResult
        시가 = self.gameFunc.시가
        종가 = self.gameFunc.종가
        고가 = self.gameFunc.고가
        저가 = self.gameFunc.저가
        시가총액 = self.gameFunc.시가총액
        거래량 = self.gameFunc.거래량
{}

def Run(parameters):
    game = 전략(parameters)
    return game.Run()

if __name__ == '__main__':
    ConditionManager().Run(Run)
""".format(self.model.dayFrom, self.model.dayTo, str(self.model.isModified), pycode))

        f.close()

        self.model.process.start('python',['tmp/tmp.py'])