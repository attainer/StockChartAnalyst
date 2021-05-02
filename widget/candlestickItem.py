import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.datas = data  ## data must have fields: time, open, close, min, max
        self.point = ""
        self.generatePicture()
        self.informViewBoundsChanged()

    def set_data(self, data, point = ""):
        self.datas = data
        self.point = point 
        self.generatePicture()
        self.informViewBoundsChanged()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        w = 1 / 3.
        t = -1
        point = t

        minimum = 9999999
        maximum = 0

        for data in self.datas:
            t = t + 1
            open = data['open']
            close = data['close']
            min = data['low']
            max = data['high']

            if minimum > min:
                minimum = min

            if maximum < max:
                maximum = max

            if open > close:
                p.setBrush(pg.mkBrush('b'))
                p.setPen(pg.mkPen('b'))
            else:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))

            delta = close - open

            if delta == 0:
                p.drawLine(QtCore.QPointF(t - 1 / 7., open), QtCore.QPointF(t + 2 / 7., open))
            else:
                p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
                p.drawRect(QtCore.QRectF(t - 1 / 7., open, 2 / 7., delta))

            if str(data['date']) == self.point:
                point = t

        if point != -1:
            p.setPen(pg.mkPen(127, 127, 127, 100))
            p.setBrush(pg.mkBrush(127, 127, 127, 100))
            p.drawRect(QtCore.QRectF(point - 1 / 7., minimum, 2 / 7., abs(minimum - maximum)))

        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())