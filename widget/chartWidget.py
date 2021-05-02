import pyqtgraph as pg
from chartPlot import ChartPlot
from PyQt5 import *

class ChartWidget(pg.GraphicsWindow):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOptions(antialias=True)
    def getTooltipText(self, x, y):
        return 'x=%f\nY=%f'%(x, y)

    def setTool(self, tooltip):
        self.tooltip = tooltip

    def setSlider(self, slider):
        self.slider = slider
        self.slider.valueChanged.connect(self.translateChart)

    def convertMousePosToXIndex(self, pos):
        result = 0
        if self.plot.sceneBoundingRect().contains(pos):
            result = self.plot.vb.mapSceneToView(pos).x()
        elif self.plot2.sceneBoundingRect().contains(pos):
            result = self.plot2.vb.mapSceneToView(pos).x()
        
        return int(round(result))

    def convertMousePosToYIndex(self, pos):
        result = 0
        if self.plot.sceneBoundingRect().contains(pos):
            result = self.plot.vb.mapSceneToView(pos).y()

        return int(round(result))

    def mousePressEvent(self, event):
        pg.GraphicsWindow.mousePressEvent(self, event)

        self.start = event.pos()
        self.isClick = True
        self.isDrag = False
        self.currentPercent = 0

    def mouseMoveEvent(self, event):
        pg.GraphicsWindow.mouseMoveEvent(self, event)
        for plot in self.plots:
            plot.onMouseMove(event.pos())
        if self.isClick == True and self.isDrag == False:
            self.isClick = False
            self.isDrag = True

            for plot in self.plots:
                plot.onDragStart(event.pos())

        if self.isDrag == True and self.mode == 'calc':
            startPoint = self.convertMousePosToYIndex(self.start)
            endPoint = self.convertMousePosToYIndex(event.pos())

            if startPoint != 0 and endPoint != 0:
                self.currentPercent = round((endPoint - startPoint) / float(startPoint) * 100, 2)

        pos = event.pos()
        isShow = False
        for plot in self.plots:
            if plot.isPosInScene(pos):
                mapPos = plot.getPosInScene(pos)
                self.tooltip.setText(self.getTooltipText(mapPos.x(), mapPos.y()))
                isShow = True
                break

        if isShow:
            bound = plot.sceneBoundingRect()

            posX = min(bound.width() + bound.x() - self.tooltip.width(), pos.x() + 30)
            posY = pos.y() - 30

            self.tooltip.move(posX, posY)
            self.tooltip.show()
            self.tooltip.move(posX, posY)
        else:
            self.tooltip.hide()

        self.tooltip.adjustSize()

    def mouseReleaseEvent(self, event):
        pg.GraphicsWindow.mouseReleaseEvent(self, event)

        self.end = event.pos()

        delta = self.start - self.end

        if self.isClick == True:
            if event.button() == QtCore.Qt.RightButton:
                self.updateRange(0, len(self.data))

        elif self.isDrag == True:
            for plot in self.plots:
                plot.onDragEnd(event.pos())

            if delta.x() != 0 and delta.y() != 0:
                if self.mode == 'zoom':
                    startPoint = self.convertMousePosToXIndex(self.start)
                    endPoint = self.convertMousePosToXIndex(self.end)

                    start = min(startPoint, endPoint)
                    end = max(startPoint, endPoint)

                    self.updateRange(int(start), int(end))

        self.isClick = False
        self.isDrag = False

    def wheelEvent(self,event):
        delta = int(event.angleDelta().y()/16)
        currentRange = self.plot.getAxis('bottom').range

        start = currentRange[0]
        end = currentRange[1]

        start += delta
        if start < 0:
            end -= delta
            start = 0
        if start > len(self.data) - 1:
            start = len(self.data) - 1
        if end > len(self.data):
            end = len(self.data)

        self.updateRange(start, end)

    def updateRange(self, start, end):
        start = int(round(start))
        end = int(round(end))
        if (len(self.data) > 0):
            self.plot.setXRange(start, end, padding=0)
            self.plot2.setXRange(start, end, padding=0)
            self.currentStart = start
            self.currentEnd = end
            
            self.slider.setMaximum(len(self.data) - (end - start))
            self.slider.setValue(start)

            if len(self.data) >= end:
                data = self.data[start:end]

                priceMin = 999999999
                priceMax = 0
                volumeMax = 0

                for i in data:
                    if priceMax < i['high']:
                        priceMax = i['high']
                    if priceMin > i['low']:
                        priceMin = i['low']
                    if volumeMax < i['volume']:
                        volumeMax = i['volume']

                self.plot.setYRange(priceMin, priceMax)
                self.plot2.setYRange(0, volumeMax)

    def translateChart(self):
        value = self.slider.value()
        current = self.plot.getAxis('bottom').range
        delta = value - self.currentStart
        
        if self.currentStart != value:
            start = self.currentStart + delta
            end = self.currentEnd + delta
            self.updateRange(start, end)


    def newPlot(self):
        plot = ChartPlot()
        self.addItem(plot, len(self.plots), 0)
        self.ci.layout.setRowStretchFactor(len(self.plots), 1)
        self.plots.append(plot)

        return plot

    def changeMode(self, mode):
        if mode == 'zoom':
            for plot in self.plots:
                plot.dragMode = 'v'
        elif mode == 'calc':
            for plot in self.plots:
                plot.dragMode = 'h'

        self.mode = mode

    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs) 

        self.currentStart = 0
        self.currentEnd = 0   

        self.setParent(parent)

        self.plots = []

        self.plot = self.newPlot()
        self.plot2 = self.newPlot()

        for plot in self.plots[:-1]:
            plot.setXLink(self.plots[-1])
            plot.getAxis('bottom').setStyle(showValues=False)

        self.ci.layout.setRowStretchFactor(0, 2)

        self.isClick = False
        self.isDrag = False
        self.mode = 'zoom'
        self.currentPercent = 0

        self.data = []

        self.setMouseTracking(True)