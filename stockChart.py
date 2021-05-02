from stockDB import StockDB
import pymongo
import datetime

class StockChart:
    def __init__(self, stockDB = None):
        self.stockDB = stockDB
    def getDayChart(self, code, fromDate, toDate):
        info = self.stockDB.info.find_one({"code" : code})

        isNeedUpdate = False
        prevFrom = 9999999999
        prevTo = 0
        currentFrom = fromDate
        currentTo = toDate

        if info == None:
            isNeedUpdate = True
        else:
            prevFrom = info["lastFrom"]
            prevTo = info["lastTo"]

            if currentFrom >= prevFrom and currentFrom <= prevTo:
                currentFrom = prevTo

            if currentTo >= prevFrom and currentTo <= prevTo:
                currentTo = prevFrom

            if (currentFrom < currentTo or 
                (currentFrom == currentTo and currentFrom != prevFrom and currentTo != prevTo)):
                isNeedUpdate = True

        #if isNeedUpdate:
        #    print('Need Update Error. {} {} {}'.format(code, fromDate, toDate))
        return list(self.stockDB.dayChart.find({"code" : code, "date" : { "$gte" : fromDate, "$lte" : toDate}}))

    def getCombinedMinChart(self, data, period):
        if len(data) == 0 or 'fail' in data[0]:
            return []

        newData = []

        i = 0
        while i < len(data):
            start = i
            back = min(i + period, len(data))

            curTime = data[i]['time'] - 1 + period

            if curTime % 100 == 60:
                curTime = curTime - 60 + 100

            curData = {
                'date': data[i]['date'],
                'time': curTime,
                'open': data[i]['open'],
                'high': data[i]['high'],
                'low': data[i]['low'],
                'close': data[i]['close'],
                'volume': data[i]['volume'],
                'buy': data[i]['buy'],
                'sell': data[i]['sell']
            }

            i = i + 1

            while i < back:
                appendData = data[i];
                if curData['date'] != appendData['date']:
                    break

                if curData['high'] < appendData['high']:
                    curData['high'] = appendData['high']
                if curData['low'] > appendData['low']:
                    curData['low'] = appendData['low']
                curData['volume'] += appendData['volume']
                curData['buy'] += appendData['buy']
                curData['sell'] += appendData['sell']

                i = i + 1

            curData['close'] = data[i - 1]['close']
            newData.append(curData)

        return newData

    def getCombinedDayToWeekChart(self, data):
        if len(data) == 0 or 'fail' in data[0]:
            return []

        currentDay = -1
        newData = []

        for i in range(data):
            current = data[i]
            weekDay = datetime.datetime(current).weekDay()
            if currentDay <= weekDay:
                newData.append(current)
                currentDay = weekDay
            else:

                if newData[-1]['high'] < current['high']:
                    newData[-1]['high'] = current['high']
                if newData[-1]['low'] > current['low']:
                    newData[-1]['low'] = current['low']
                newData[-1]['volume'] += current['volume']
                newData[-1]['cap'] += current['cap']
                newData[-1]['close'] = current['close']

        return newData

    def getMinChart(self, code, fromDate, toDate, period = 1):

        info = self.stockDB.minInfo.find_one({"code" : code})

        isNeedUpdate = False
        prevFrom = 9999999999
        prevTo = 0
        currentFrom = fromDate
        currentTo = toDate

        if info == None:
            isNeedUpdate = True
        else:
            prevFrom = info["lastFrom"]
            prevTo = info["lastTo"]

            if currentFrom >= prevFrom and currentFrom <= prevTo:
                currentFrom = prevTo

            if currentTo >= prevFrom and currentTo <= prevTo:
                currentTo = prevFrom

            if (currentFrom < currentTo or 
                (currentFrom == currentTo and currentFrom != prevFrom and currentTo != prevTo)):
                isNeedUpdate = True

        if isNeedUpdate:
            print('Need Update Error. {} {} {}'.format(code, fromDate, toDate))
        data = list(self.stockDB.db[code].find({ "date" : { "$gte" : fromDate, "$lte" : toDate}}))
        result = self.getCombinedMinChart(data, period)

        return result
if __name__ == "__main__":
    data = StockChart(StockDB()).getMinChart('A000040', 20180529, 5)
    for i in data:
        print(i)