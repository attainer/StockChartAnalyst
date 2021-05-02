import win32com.client
import time
from stockDB import StockDB
import datetime

class StockChartInternet:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    # 차트 요청 - 기간 기준으로
    def RequestFromTo(self, code, fromDate, toDate, type, period = 1):

        data = []
 
        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.objStockChart.SetInputValue(2, toDate)  # To 날짜
        self.objStockChart.SetInputValue(3, fromDate)  # From 날짜
        if type == "m":
            self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 37])  # 날짜,시가,고가,저가,종가,거래량, 매도, 매수
        else:
            self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 10, 11, 13, 37])  # 날짜,시가,고가,저가,종가,거래량, 매도, 매수, 시가총액
        self.objStockChart.SetInputValue(6, ord(type))  # '차트 주기 - 일간 차트 요청
        self.objStockChart.SetInputValue(7, period)  # '차트 주기 - 일간 차트 요청

        self.objStockChart.SetInputValue(9, ord('0'))  # 수정주가 사용
        self.objStockChart.SetInputValue(10, ord('3'))  # 수정주가 사용
        self.objStockChart.BlockRequest()
        length = self.objStockChart.GetHeaderValue(3)

        buySell = []

        for i in range(length):
            data.append({
                'code' : code,
                'date' : int(self.objStockChart.GetDataValue(0, i)),
                'time' : int(self.objStockChart.GetDataValue(1, i)),
                'open' : self.objStockChart.GetDataValue(2, i),
                'high' : self.objStockChart.GetDataValue(3, i),
                'low' : self.objStockChart.GetDataValue(4, i),
                'close' : self.objStockChart.GetDataValue(5, i),
                'volume' : self.objStockChart.GetDataValue(7, i),
                'buy' : self.objStockChart.GetDataValue(9, i),
                'sell' : self.objStockChart.GetDataValue(8, i),
                })
            if type != "m":
                data[-1]['prev'] = data[-1]['close'] - self.objStockChart.GetDataValue(6, i)
                data[-1]['cap'] = self.objStockChart.GetDataValue(10, i)
        time.sleep(0.25)

        data = data[::-1]

        if len(data) == 0:
            return data


        if type == 'm': 
            prevBuy = 0
            prevSell = 0

            for i in range(len(data)):
                if i > 0 and data[i-1]['date'] != data[i]['date']:
                    prevBuy = 0
                    prevSell = 0
                
                currentBuy = data[i]['buy']
                currentSell = data[i]['sell']

                data[i]['buy'] = currentBuy - prevBuy
                data[i]['sell'] = currentSell - prevSell

                prevBuy = currentBuy
                prevSell = currentSell

            data2 = [data[0]]

            for i in range(1, len(data)):
                if data[i]['date'] == data[i-1]['date']:
                    hh, mm = divmod(data[i]['time'], 100)
                    curTime = hh * 60 + mm

                    hh, mm = divmod(data[i-1]['time'], 100)
                    beforeTime = hh * 60 + mm

                    delta = curTime - beforeTime

                    for j in range(period, delta, period):
                        newTime = beforeTime + j
                        hh = int(newTime / 60) * 100
                        mm = newTime % 60
                        newTime = hh + mm

                        data2.append({
                            'code' : code,
                            'date' : data[i-1]['date'],
                            'time' : newTime,
                            'open' : data[i-1]['close'],
                            'high' : data[i-1]['close'],
                            'low' : data[i-1]['close'],
                            'close' : data[i-1]['close'],
                            'volume' : 0,
                            'buy' : 0,
                            'sell' : 0
                        })
                data2.append(data[i])

            data = data2

        return data

    def getCombinedDayToWeekChart(self, data):
        if len(data) == 0 or 'fail' in data[0]:
            return []

        currentDay = 9
        newData = []

        for current in data:
            year = int(current['date'] / 10000)

            month = int((current['date'] % 10000) / 100)
            day = int((current['date'] % 100))
            weekday = datetime.datetime(year, month, day).weekday()
            if currentDay >= weekday:
                newData.append(current)
                currentDay = weekday
                print(weekday)
            else:

                if newData[-1]['high'] < current['high']:
                    newData[-1]['high'] = current['high']
                if newData[-1]['low'] > current['low']:
                    newData[-1]['low'] = current['low']
                newData[-1]['volume'] += current['volume']
                newData[-1]['cap'] += current['cap']
                newData[-1]['close'] = current['close']
                currentDay = weekday

        return newData

if __name__ == "__main__":
    data = StockChartInternet().RequestFromTo('A005930', 20180501, 20180530, 'm', 1)

    for i in data:
        print(i)