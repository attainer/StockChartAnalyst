from stockDB import StockDB
from multiprocessing import Pool
import pathlib

class ConditionManager:
    def __init__(self):
        self.results = {};

    def CombineResult(self, results):
        for result in results:
            for key, value in result.items():
                if key not in self.results:
                    self.results[key] = value
                else:
                    self.results[key] += value

    def ShowResult(self, totalCnt):
        for key, value in self.results.items():
            print("{}, 총 발생: {}, 산술평균: {:.2%}, 기하평균: {:.2%}, 발생확률: {:.1%}".format(key, value.count, value.sum / value.count - 1, value.mul ** (1. / value.count) - 1, value.count / totalCnt));

            pathlib.Path("result").mkdir(exist_ok=True)
            f = open("result/" + key + ".txt", "w")
            for text in value.data:
                f.write(text + '\n')
            f.close();

        print("총 테스트 케이스: {}".format(totalCnt));

    def Run(self, func):
        db = StockDB();
        infoList = list(db.info.find())
        n = 8;
        p = Pool(n)

        codeList = []
        for info in infoList:
            if "group" not in info:
                continue
            codeList.append([info['code'], info['group']])

        divider = int(len(codeList) / n) + 1
        codeLists = chunks(codeList, divider)

        results = p.map(func, codeLists)
        #results = [func(codeList)]
        totalCnt = 0
        totalResults = []

        for result in results:
            totalCnt += result[0]
            totalResults.append(result[1])

        self.CombineResult(totalResults)
        self.ShowResult(totalCnt)

    def exRun(parameters):
        game = 전략(parameters)
        return game.Run()

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    ConditionManager().Run()