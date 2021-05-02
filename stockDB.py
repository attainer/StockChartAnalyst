import pymongo

class StockDB:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.stock

        self.info = self.db.info
        self.minInfo = self.db.minInfo
        self.dayChart = self.db.dayChart

        self.info.create_index([('code', pymongo.ASCENDING)], unique=True)
        self.minInfo.create_index([('code', pymongo.ASCENDING)], unique=True)
        self.dayChart.create_index([('code', pymongo.ASCENDING), ('date', pymongo.ASCENDING)], unique=True)
        #self.minChart.create_index([('code', pymongo.ASCENDING), ('date', pymongo.ASCENDING), ('time', pymongo.ASCENDING)], unique=True)



if __name__ == "__main__":
    pass
#    chart = StockChart(StockDB())
#    print(chart.getDayChart("A000040", 20180201, 20180219))
#    print(chart.getMinChart("A000040", 20180213, 5))