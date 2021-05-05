import sys
import copy

from stockChart import StockChart
from stockDB import StockDB
from gameFunc import GameFunc, ConditionOutOfIndexException

class Result:
    def __init__(self):
        self.data = []
        self.sum = 0
        self.mul = 1.0
        self.money = 1.0
        self.count = 0

    def __add__(self, other):
        newData = Result()
        newData.data = self.data + other.data
        newData.sum = self.sum + other.sum
        newData.mul = self.mul * other.mul
        newData.money = self.money * other.money
        newData.count = self.count + other.count

        return newData

class GameManager:
    def __init__(self, parameters):
        self.stockChart = StockChart(StockDB())
        self.codeList = parameters
        self.results = {}
        self.resultCnt = 0
        self.minCharts = {}
        self.fromDate = 0
        self.toDate = 0
        self.isModified = False

    def Run(self):
        for code in self.codeList:
            print(code[0])
            sys.stdout.flush()

            self.code = code[0]
            self.group = code[1]

            dayChart = self.stockChart.getDayChart(self.code, self.fromDate, self.toDate)
            self.gameFunc = GameFunc(self.group, dayChart, self.isModified)

            for i in range(len(dayChart)):
                if (self.gameFunc.일봉(i)['volume'] == 0):
                    continue
                try:
                    self.Strategy(i);
                except ConditionOutOfIndexException:
                    pass

        return (self.resultCnt, self.results)

    def setResult(self, key):
        self.results[key] = Result()

    def addResult(self, key, 일봉, value):
        date = 일봉['date']
        if key not in self.results:
            self.setResult(key);

        self.results[key].sum += value
        self.results[key].mul *= value
        self.results[key].count += 1
        self.results[key].money *= (value)

        self.results[key].data.append(self.code + ' ' + str(date))

    def addCase(self):
        self.resultCnt += 1

if __name__ == "__main__":
    ConditionManager().Run()