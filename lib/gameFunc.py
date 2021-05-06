import sys
import copy

from stockChart import StockChart
from stockDB import StockDB

class ConditionOutOfIndexException(Exception):
    pass

class GameFunc:
    def __init__(self, stockChart, group, chart, isModified):
        self.group = group
        self.stockChart = stockChart
        self.chart = chart if not isModified else self.getModifiedChart(chart)
        self.preChart = chart

        self.minCharts = {}

    def 시가(self, x):
        return self.일봉(x)['open']

    def 고가(self, x):
        return self.일봉(x)['high']

    def 종가(self, x):
        return self.일봉(x)['close']

    def 저가(self, x):
        return self.일봉(x)['low']

    def 거래량(self, x):
        return self.일봉(x)['volume']

    def 시가총액(self, x):
        return self.일봉(x)['cap']

    def 전일종가(self, x):
        return self.일봉(x)['prev']

    def 날짜(self, x):
        return self.일봉(x)['date']

    def 일봉(self, x):
        if x >= len(self.chart) or x < 0:
            raise ConditionOutOfIndexException()
        return self.chart[x]

    def 분봉(self, x):
        if x in self.minCharts:
            return self.minCharts[x]
        else:
            minChart = self.stockChart.getMinChart(self.code, self.chart[x]['date'], self.chart[x]['date'], 1)
            self.minCharts[x] = minChart
            return minChart

    def 상한가(self, x):
        current = self.preChart[x]
        if current['high'] / current['prev'] > 1.28 and current['volume'] > 100000:
            curHoga = current['prev'];
            while True:
                curHoga2 = self.GetNextHoga(curHoga, 1, self.group);
                if curHoga2 / current['prev'] > 1.3000001:
                    break
                curHoga = curHoga2

            if (curHoga == current['close']):
                return True
        return False

    def GetNextHoga(self, price, n, group):
        for i in range(n):
            if price < 1000:
                price += 1;
            elif price < 5000:
                price += 5
            elif price < 10000:
                price += 10
            elif price < 50000:
                price += 50
            else:
                if group == "d" or price < 100000:
                    price += 100;
                elif price < 500000:
                    price += 500
                else:
                    price += 1000
        return price

    def GetPrevHoga(self, price, n):
        for i in range(n):
            if price < 1000:
                price -= 1;
            elif price < 5000:
                price -= 5
            elif price < 10000:
                price -= 10
            elif price < 50000:
                price -= 50
            elif price < 100000:
                price -= 100
            elif price < 500000:
                price -= 500
            else:
                price -= 1000
        return price

    def IsStay(self, data, price ):
        if  (data['open'] == price and 
            data['high'] == price and
            data['low'] == price and
            data['close'] == price):
                return True
        else:
            return False

    def getAveLine(self, datas, n):
        closeList = []
        for data in datas:
            closeList.append(data['close'])

        aveList = []
        for i in range(len(closeList) - n + 1):
            data = closeList[i:i+n]

            ave = sum(data) / float(len(data))
            aveList.append(ave)

        return aveList

    def maximum(self, datas, key):
        max = 0
        for data in datas:
            if data[key] > max:
                max = data[key]

        return max

    def minimum(self, datas, key):
        max = 9999999
        for data in datas:
            if data[key] < max:
                max = data[key]

        return max

    def getModifiedChart(self, chart):
        chart = copy.deepcopy(chart);
        length = len(chart)

        if length <= 0:
            return chart

        last = chart[-1]

        for i in range(length - 1, 0, -1):
            current = chart[i]['prev']
            prev = chart[i - 1]['close']

            if current != prev:

                ratio = current / float(prev)
                
                chart[i - 1]['open'] *= ratio
                chart[i - 1]['close'] *= ratio
                chart[i - 1]['high'] *= ratio
                chart[i - 1]['low'] *= ratio
                chart[i - 1]['prev'] *= ratio
                chart[i - 1]['volume'] /= ratio
                chart[i - 1]['buy'] /= ratio
                chart[i - 1]['sell'] /= ratio

        return chart

if __name__ == "__main__":
    ConditionManager().Run()