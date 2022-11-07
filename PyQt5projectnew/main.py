import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.brushcolor = Qt.black
        self.fillcolor = QColor(0, 0, 0, 0)
        self.brushsize = 1
        self.instrument = 'Brush'
        self.undo = []
        self.redo = []
        self.x = 512
        self.y = 512
        self.resize(self.x, self.y)
        self.setAttribute(Qt.WA_StaticContents)
        self.currentImage = QImage(self.size(), QImage.Format_RGB32)
        self.currentImage.fill(QColor(255, 255, 255))

    def copy_for_draw(self):
        self.copy = QImage(self.currentImage.size(), QImage.Format_RGB32)
        self.copy.fill(QColor(255, 255, 255))
        painter = QPainter(self.copy)
        painter.drawImage(QPoint(0, 0), self.currentImage)

    def copy_for_undo(self):
        copy = QImage(self.currentImage.size(), QImage.Format_RGB32)
        copy.fill(QColor(255, 255, 255))
        painter = QPainter(copy)
        painter.drawImage(QPoint(0, 0), self.currentImage)
        return copy

    def undo_check(self):
        Window.undo_button.setEnabled(True)
        if len(self.undo) < 10:
            self.undo.append(self.copy_for_undo())
        else:
            self.undo.pop(0)
            self.undo.append(self.copy_for_undo())

    def redo_check(self):
        if len(self.redo) < 10:
            self.redo.append(self.copy_for_undo())
        else:
            self.redo.pop(0)
            self.redo.append(self.copy_for_undo())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.currentImage, self.rect())

    def mousePressEvent(self, event):
        self.copy_for_draw()
        self.undo_check()
        if event.button() == Qt.RightButton:
            self.lastPoint = QPoint(event.pos())
        elif self.instrument == 'Brush' and event.button() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.lastPoint = QPoint(event.pos())
            painter.drawPoint(self.lastPoint)
            self.update()
        elif self.instrument == 'Eraser' and event.button() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(QColor(255, 255, 255), self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.lastPoint = QPoint(event.pos())
            painter.drawPoint(self.lastPoint)
            self.update()
        elif self.instrument == 'Line' and event.button() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.lastPoint = QPoint(event.pos())
            painter.drawPoint(self.lastPoint)
            self.update()
        elif self.instrument == 'Ellipse' and event.button() == Qt.LeftButton:
            self.lastPoint = QPoint(event.pos())
        elif self.instrument == 'Rect' and event.button() == Qt.LeftButton:
            self.lastPoint = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            painter = QPainter(self.currentImage)
            painter.drawImage(QPoint(0, 0), self.copy)
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRect(self.lastPoint.x(), self.lastPoint.y(), event.x() - self.lastPoint.x(),
                             event.y() - self.lastPoint.y())
            self.update()
        elif self.instrument == 'Brush' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = QPoint(event.pos())
            self.update()
        elif self.instrument == 'Line' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.drawImage(QPoint(0, 0), self.copy)
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.update()
        elif self.instrument == 'Ellipse' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.drawImage(QPoint(0, 0), self.copy)
            painter.setBrush(QBrush(self.fillcolor))
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawEllipse(self.lastPoint, event.x() - self.lastPoint.x(), event.y() - self.lastPoint.y())
            self.update()
        elif self.instrument == 'Rect' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.drawImage(QPoint(0, 0), self.copy)
            painter.setBrush(QBrush(self.fillcolor))
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRect(self.lastPoint.x(), self.lastPoint.y(), event.x() - self.lastPoint.x(),
                             event.y() - self.lastPoint.y())
            self.update()
        elif self.instrument == 'Eraser' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(QColor(255, 255, 255), self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = QPoint(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            painter = QPainter(self.currentImage)
            painter.drawImage(QPoint(0, 0), self.copy)
            self.update()
            piece = self.currentImage.copy(self.lastPoint.x(), self.lastPoint.y(), event.x() - self.lastPoint.x(),
                             event.y() - self.lastPoint.y())
            fname = QFileDialog.getSaveFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            if fname != "":
                piece.save(fname)
        if self.instrument == 'Line' and event.button == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.update()
        elif self.instrument == 'Ellipse' and event.button == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setBrush(QBrush(self.fillcolor))
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawEllipse(self.lastPoint, event.x() - self.lastPoint.x(), event.y() - self.lastPoint.y())
            self.update()
        elif self.instrument == 'Rect' and event.button == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setBrush(QBrush(self.fillcolor))
            painter.setPen(QPen(self.brushcolor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRect(self.lastPoint.x(), self.lastPoint.y(), event.x() - self.lastPoint.x(),
                             event.y() - self.lastPoint.y())
            self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create Canvas
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('PyQt5 Paint')
        self.setWindowIcon(QIcon('icons/Main.png'))
        self.setGeometry(0, 0, self.canvas.x + 100, self.canvas.y + 120)
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
        self.actionEraser = QAction(QIcon('icons/eraser.png'), 'Eraser')
        self.actionOpen = QAction(QIcon('icons/open.png'), 'Open')
        self.actionClear = QAction('Clear')
        self.actionBrush.triggered.connect(self.chooseBrush)
        self.actionLine.triggered.connect(self.chooseLine)
        self.actionCircle.triggered.connect(self.chooseEllipse)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionRect.triggered.connect(self.chooseRect)
        self.actionEraser.triggered.connect(self.chooseEraser)
        self.actionOpen.triggered.connect(self.OpenImage)
        self.actionClear.triggered.connect(self.clear)

        self.button_1 = QPushButton(self)
        self.button_1.setText("COlOR_1")
        self.button_1.clicked.connect(self.color1)

        self.button_2 = QPushButton(self)
        self.button_2.setText("COlOR_2")
        self.button_2.clicked.connect(self.color2)

        self.undo_button = QPushButton(self)
        self.undo_button.setText("Undo")
        self.undo_button.clicked.connect(self.undo)
        self.undo_button.setEnabled(False)

        self.redo_button = QPushButton(self)
        self.redo_button.setText('Redo')
        self.redo_button.clicked.connect(self.redo)
        self.redo_button.setEnabled(False)

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
        self.toolsmenu.addAction(self.actionEraser)
        self.toolsmenu.addAction(self.actionClear)
        self.shapesmenu.addAction(self.actionLine)
        self.shapesmenu.addAction(self.actionCircle)
        self.shapesmenu.addAction(self.actionRect)

        self.toolbar.addAction(self.actionBrush)
        self.toolbar.addAction(self.actionEraser)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionLine)
        self.toolbar.addAction(self.actionCircle)
        self.toolbar.addAction(self.actionRect)

        self.editbar.addAction(self.actionSave)
        self.editbar.addAction(self.actionExit)
        self.editbar.addAction(self.actionOpen)
        self.editbar.addSeparator()
        self.editbar.addWidget(self.undo_button)
        self.editbar.addWidget(self.redo_button)
        self.editbar.addSeparator()
        self.editbar.addWidget(self.button_1)
        self.editbar.addWidget(self.button_2)
        self.editbar.addWidget(self.filloff)
        self.editbar.addSeparator()
        self.editbar.addWidget(self.lpx)
        self.editbar.addWidget(self.SpinBoxBrushsize)

    def color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_1.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.canvas.brushcolor = color

    def color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_2.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.filloff.setText('FillON')
            self.filloff.setEnabled(True)
            self.canvas.fillcolor = color

    def undo(self):
        self.redo_button.setEnabled(True)
        painter = QPainter(self.canvas.currentImage)
        self.canvas.redo_check()
        painter.drawImage(QPoint(0, 0), self.canvas.undo[-1])
        self.canvas.update()
        self.canvas.undo.pop()
        if len(self.canvas.undo) == 0:
            self.undo_button.setEnabled(False)

    def redo(self):
        self.undo_button.setEnabled(True)
        painter = QPainter(self.canvas.currentImage)
        self.canvas.undo_check()
        painter.drawImage(QPoint(0, 0), self.canvas.redo[-1])
        self.canvas.update()
        self.canvas.redo.pop()
        if len(self.canvas.redo) == 0:
            self.redo_button.setEnabled(False)

    def Filloff(self):
        self.button_2.setStyleSheet("background-color: white")
        self.filloff.setText('FillOff')
        self.filloff.setEnabled(False)
        self.canvas.fillcolor = QColor(0, 0, 0, 0)

    def BrushSizeUpdate(self):
        self.canvas.brushsize = self.SpinBoxBrushsize.value()
        self.lpx.setText(f'{self.SpinBoxBrushsize.value()}px')

    def clear(self):
        self.canvas.currentImage.fill(QColor(255, 255, 255))
        self.canvas.update()

    def chooseBrush(self):
        self.canvas.instrument = 'Brush'

    def chooseLine(self):
        self.canvas.instrument = 'Line'

    def chooseEllipse(self):
        self.canvas.instrument = 'Ellipse'

    def chooseRect(self):
        self.canvas.instrument = 'Rect'

    def chooseEraser(self):
        self.canvas.instrument = 'Eraser'

    def closeEvent(self, event):
        message = '''Вы точно хотите выйти?\nНесохраненные данные будут потеряны.'''
        reply = QMessageBox.question(
            self, 'Предупреждение!', message,
            QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Close)

        if reply == QMessageBox.Close:
            QApplication.quit()

        elif reply == QMessageBox.Save:
            self.saveFile()

        elif reply == QMessageBox.Cancel:
            pass

    def OpenImage(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if fname != "":
            self.canvas.currentImage = QImage(fname)

    def saveFile(self):
        fname = QFileDialog.getSaveFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if fname != "":
            self.canvas.currentImage.save(fname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
