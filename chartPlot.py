import pyqtgraph as pg

class ChartPlot(pg.PlotItem):
    def onMouseMove(self, pos):
        mapPos = self.getPosInScene(pos)
        if self.isPosInScene(pos):
            self.crossLine['h'].setPos(mapPos.y())
            self.crossLine['h'].show()
        else:
            self.crossLine['h'].hide()

        self.crossLine['v'].setPos(mapPos.x())

        if self.isDragging == False:
            self.dragLine['h'].hide()
            self.dragLine['v'].hide()

    def onDragStart(self, pos):
        self.isDragging = True
        mapPos = self.getPosInScene(pos)
        if self.dragMode == 'h':
            if self.isPosInScene(pos):
                self.dragLine['h'].setPos(mapPos.y())
                self.dragLine['h'].show()
        elif self.dragMode == 'v':
            self.dragLine['v'].setPos(mapPos.x())
            self.dragLine['v'].show()

    def onDragEnd(self, pos):
        self.isDragging = False

    def changeDragMode(self, type):
        self.dragMode = type

    def isPosInScene(self, pos):
        return self.sceneBoundingRect().contains(pos)

    def getPosInScene(self, pos):
        return self.vb.mapSceneToView(pos)


    def __init__(self, *args, **kwds):
        pg.PlotItem.__init__(self, *args, **kwds)

        crossLineH = pg.InfiniteLine(angle=0, movable=False)
        crossLineV = pg.InfiniteLine(angle=90, movable=False)
        
        self.crossLine = { 'v' : crossLineV, 'h' : crossLineH }
        self.addItem(crossLineH, ignoreBounds=True)
        self.addItem(crossLineV, ignoreBounds=True)

        dragLineH = pg.InfiniteLine(angle=0, movable=False)
        dragLineV = pg.InfiniteLine(angle=90, movable=False)

        self.dragLine = { 'v' : dragLineV, 'h' : dragLineH }
        self.addItem(dragLineH, ignoreBounds=True)
        self.addItem(dragLineV, ignoreBounds=True)

        self.dragMode = 'v'
        self.isDragging = False


        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)