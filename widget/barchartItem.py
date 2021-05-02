import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

class BarchartItem(pg.GraphicsObject):
    def __init__(self, data, brushColor):
        pg.GraphicsObject.__init__(self)
        self.datas = data
        self.brushColor = brushColor
        self.generatePicture()

    def set_data(self, data):
        self.datas = data
        self.generatePicture()
        self.informViewBoundsChanged()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        t = -1

        p.setBrush(pg.mkBrush(color=self.brushColor))
        p.setPen(pg.mkPen(color=self.brushColor))
        for data in self.datas:
            t = t + 1

            p.drawRect(QtCore.QRectF(t - 1 / 3., 0, 2 / 3., data))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())