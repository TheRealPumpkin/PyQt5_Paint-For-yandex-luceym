import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class BrushPoint:
    def __init__(self, color, size, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPoint(self.x, self.y)


class Line:
    def __init__(self, color, size, sx, sy, ex, ey):
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        self.color = color
        self.size = size

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Ellipse:
    def __init__(self, color, fcolor, size, sx, sy, ex, ey):
        self.xy = QPoint(sx, sy)
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        self.color = color
        self.size = size
        self.fcolor = fcolor

    def draw(self, painter):
        rx, ry = self.ex - self.sx, self.ey - self.sy
        painter.setBrush(QBrush(self.fcolor))
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawEllipse(self.xy, rx, ry)


class Rect:
    def __init__(self, color, fcolor, size, sx, sy, ex, ey):
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        self.color = color
        self.size = size
        self.fcolor = fcolor

    def draw(self, painter):
        rx, ry = self.ex - self.sx, self.ey - self.sy
        painter.setBrush(QBrush(self.fcolor))
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(self.sx, self.sy, rx, ry)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.objects = []

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for i in self.objects:
            i.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        if Window.instrument == 'Brush':
            self.objects.append(BrushPoint(Window.brushcolor, Window.brushsize, event.x(), event.y()))
            self.update()
        elif Window.instrument == 'Line':
            self.objects.append(Line(Window.brushcolor, Window.brushsize, event.x(), event.y(), event.x(), event.y()))
            self.update()
        elif Window.instrument == 'Ellipse':
            self.objects.append(Ellipse(Window.brushcolor, Window.fillcolor, Window.brushsize, event.x(), event.y(),
                                        event.x(), event.y()))
            self.update()
        elif Window.instrument == 'Rect':
            self.objects.append(Rect(Window.brushcolor, Window.fillcolor, Window.brushsize, event.x(), event.y(),
                                        event.x(), event.y()))
            self.update()

    def mouseMoveEvent(self, event):
        if Window.instrument == 'Brush':
            self.objects.append(BrushPoint(Window.brushcolor, Window.brushsize, event.x(), event.y()))
            self.update()
        elif Window.instrument == 'Line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif Window.instrument == 'Ellipse':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif Window.instrument == 'Rect':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.brushcolor = Qt.black
        self.fillcolor = QColor(0, 0, 0, 0)
        self.brushsize = 1
        self.instrument = 'Brush'
        self.x = 960 + 72
        self.y = 960 + 94
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('PyQt5 Paint')
        self.setWindowIcon(QIcon('icons/Main.png'))
        self.setGeometry(100, 100, self.x, self.y)
        self.setFixedSize(self.x, self.y)
        self.setStyleSheet(
            """
                    QPushButton
                     {text-align : center;
                     background-color : white;
                     font: bold;
                     border-color: gray;
                     border-width: 2px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 14px;}
                     QPushButton:pressed
                     {text-align : center;
                     background-color : light gray;
                     font: bold;
                     border-color: gray;
                     border-width: 2px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 14px;}
                    """)

# Create Canvas
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

# Create menubar and toolbars
        menubar = self.menuBar()
        self.filemenu = menubar.addMenu('File')
        self.toolsmenu = menubar.addMenu('Tools')
        self.shapesmenu = menubar.addMenu('shapes')

        self.toolbar = QToolBar(self)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        self.editbar = QToolBar(self)
        self.editbar.setMovable(False)
        self.editbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.TopToolBarArea, self.editbar)


# Create actions and widgets
        self.actionSave = QAction(QIcon('icons/save.png'), 'Save')
        self.actionExit = QAction(QIcon('icons/exit.png'), 'Exit')
        self.actionBrush = QAction(QIcon('icons/brush_32.png'), 'Brush')
        self.actionLine = QAction(QIcon('icons/Line.png'), 'Line')
        self.actionCircle = QAction(QIcon('icons/Ellipse.png'), 'Ellipse')
        self.actionRect = QAction(QIcon('icons/rect.png'), 'Rect')
        self.actionOpen = QAction('Open')
        self.actionBrush.triggered.connect(self.chooseBrush)
        self.actionLine.triggered.connect(self.chooseLine)
        self.actionCircle.triggered.connect(self.chooseEllipse)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionRect.triggered.connect(self.chooseRect)


        self.button_1 = QPushButton(self)
        self.button_1.setText("COlOR_1")
        self.button_1.clicked.connect(self.color1)


        self.button_2 = QPushButton(self)
        self.button_2.setText("COlOR_2")
        self.button_2.clicked.connect(self.color2)

        self.filloff = QPushButton(self)
        self.filloff.setText('Fill Off')
        self.filloff.clicked.connect(self.Filloff)
        self.filloff.setEnabled(False)

        self.lpx = QLabel(self)
        self.lpx.setText(f'1px')

        self.SpinBoxBrushsize = QSpinBox(self)
        self.SpinBoxBrushsize.setFocusPolicy(Qt.NoFocus)
        self.SpinBoxBrushsize.setMinimum(1)
        self.SpinBoxBrushsize.setMaximum(50)
        self.SpinBoxBrushsize.valueChanged.connect(self.BrushSizeUpdate)


# Add actions and widgets to menubar and toolbars
        self.filemenu.addAction(self.actionSave)
        self.filemenu.addAction(self.actionExit)
        self.filemenu.addAction(self.actionOpen)
        self.toolsmenu.addAction(self.actionBrush)
        self.shapesmenu.addAction(self.actionLine)
        self.shapesmenu.addAction(self.actionCircle)
        self.shapesmenu.addAction(self.actionRect)

        self.toolbar.addAction(self.actionBrush)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionLine)
        self.toolbar.addAction(self.actionCircle)
        self.toolbar.addAction(self.actionRect)

        self.editbar.addAction(self.actionSave)
        self.editbar.addAction(self.actionExit)
        self.editbar.addSeparator()
        self.editbar.addWidget(self.button_1)
        self.editbar.addWidget(self.button_2)
        self.editbar.addWidget(self.filloff)
        self.editbar.addSeparator()
        self.editbar.addWidget(self.lpx)
        self.editbar.addWidget(self.SpinBoxBrushsize)

    def saveFile(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', "C:\\", "Portable Network Graphic (*.png)")
        if (name[0] != ""):
            fCheck = os.path.splitext(name[0])
            fCheck = fCheck[1]
            feCheck = fCheck[1:].upper()
            print(feCheck)
            canv = QPixmap(self.canvas.size())
            self.canvas.render(canv)
            canv.save(name[0], feCheck)
            drawingName = os.path.basename(name[0])
            self.setWindowTitle(drawingName + " - Painting v0.1pa")

    def color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_1.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.brushcolor = color

    def color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_2.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.filloff.setText('FillON')
            self.filloff.setEnabled(True)
            self.fillcolor = color

    def Filloff(self):
        self.button_2.setStyleSheet("background-color: white")
        self.filloff.setText('FillOff')
        self.filloff.setEnabled(False)
        self.fillcolor = QColor(0, 0, 0, 0)

    def BrushSizeUpdate(self):
        self.brushsize = self.SpinBoxBrushsize.value()
        self.lpx.setText(f'{self.SpinBoxBrushsize.value()}px')

    def chooseBrush(self):
        self.instrument = 'Brush'

    def chooseLine(self):
        self.instrument = 'Line'

    def chooseEllipse(self):
        self.instrument = 'Ellipse'

    def chooseRect(self):
        self.instrument = 'Rect'

    def closeEvent(self, event):
        text = '''Are you sure you want to Quit?\nAny unsaved work will be lost.'''
        reply = QMessageBox.question(
            self, 'Warning!', text,
            QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Close)

        if reply == QMessageBox.Close:
            QApplication.quit()

        elif reply == QMessageBox.Save:
            self.saveFile()

        elif reply == QMessageBox.Cancel:
            pass

    def Open(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())