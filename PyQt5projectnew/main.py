import sys

from random import gauss
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
# Стандартные значения
        self.brushcolor = Qt.black
        self.fillcolor = QColor(0, 0, 0, 0)
        self.brushsize = 1
        self.instrument = 'Brush'
# Параметры для распылителя(пока фиксированные)
        self.spray_diametr = 12
        self.spray_count_of_points = 120
# Откат и возврат действий
        self.undo = []
        self.redo = []
# Размеры поля, пока фиксированые
        self.x = 1024
        self.y = 720
        self.resize(self.x, self.y)
        self.currentImage = QImage(self.size(), QImage.Format_RGB32)
        self.currentImage.fill(QColor(255, 255, 255))

# Рисование
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
        elif self.instrument == 'Spray' and event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
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
        elif self.instrument == 'Spray' and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.currentImage)
            painter.setPen(QPen(self.brushcolor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for i in range(self.spray_count_of_points):
                x = gauss(0, self.spray_diametr)
                y = gauss(0, self.spray_diametr)
                painter.drawPoint(int(self.lastPoint.x() + x), int(self.lastPoint.y() + y))
            self.lastPoint = event.pos()
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
            self.savepiece(event)
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

# Вырезка, но недопиленная
    def savepiece(self, event):
        painter = QPainter(self.currentImage)
        painter.drawImage(QPoint(0, 0), self.copy)
        self.update()
        piece = self.currentImage.copy(self.lastPoint.x(), self.lastPoint.y(), event.x() - self.lastPoint.x(),
                                       event.y() - self.lastPoint.y())
        fname = QFileDialog.getSaveFileName(
            self, 'Save file', '',
            'Format (*.jpg);;Format (*.png)')[0]
        if fname != "":
            piece.save(fname)

# Работа с полем для рисования
    def clearUnRedo(self):
        self.undo.clear()
        Window.undo_button.setEnabled(False)
        self.redo.clear()
        Window.redo_button.setEnabled(False)

    def setStandartValues(self):
        self.brushcolor = Qt.black
        self.fillcolor = QColor(0, 0, 0, 0)
        self.brushsize = 1
        self.instrument = 'Brush'

    def new(self):
        self.clearUnRedo()
        self.setStandartValues()
        Window.setStartValues()
        self.resize(self.x, self.y)
        self.currentImage = QImage(self.size(), QImage.Format_RGB32)
        self.currentImage.fill(QColor(255, 255, 255))
        self.update()

    def open(self, fname):
        loadImage = QImage(fname)
        self.clearUnRedo()
        if loadImage.width() > self.x or loadImage.height() > self.y:
            self.currentImage = loadImage.scaled(1024, 720, Qt.KeepAspectRatio)
        else:
            self.currentImage = loadImage

# Копия для отображения фигур при их построении
    def copy_for_draw(self):
        self.copy = QImage(self.currentImage.size(), QImage.Format_RGB32)
        self.copy.fill(QColor(255, 255, 255))
        painter = QPainter(self.copy)
        painter.drawImage(QPoint(0, 0), self.currentImage)

# Реализация отката действий
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

# Реализация возврата действий
    def redo_check(self):
        if len(self.redo) < 10:
            self.redo.append(self.copy_for_undo())
        else:
            self.redo.pop(0)
            self.redo.append(self.copy_for_undo())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('PyQt5 Paint')
        self.setWindowIcon(QIcon('icons/Main.png'))
        self.setGeometry(0, 0, 1024 + 100, 720 + 120)
        self.setMinimumSize(1024 + 100, 720 + 120)

# Здесь когда_нибудь будет красивый интерфейс, но пока только кнопки
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
        self.shapesmenu = menubar.addMenu('Shapes')
        self.helpmenu = menubar.addMenu('Help')

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
        self.actionNew = QAction('New')
        self.actionBrush = QAction(QIcon('icons/brush_32.png'), 'Brush')
        self.actionSpray = QAction(QIcon('icons/spray.png'), 'Spray')
        self.actionLine = QAction(QIcon('icons/Line.png'), 'Line')
        self.actionCircle = QAction(QIcon('icons/Ellipse.png'), 'Ellipse')
        self.actionRect = QAction(QIcon('icons/rect.png'), 'Rect')
        self.actionEraser = QAction(QIcon('icons/eraser.png'), 'Eraser')
        self.actionOpen = QAction(QIcon('icons/open.png'), 'Open')
        self.actionClear = QAction('Clear')
        self.actionInfo = QAction('Info')
        self.actionBrush.triggered.connect(self.chooseBrush)
        self.actionSpray.triggered.connect(self.chooseSpray)
        self.actionLine.triggered.connect(self.chooseLine)
        self.actionCircle.triggered.connect(self.chooseEllipse)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionRect.triggered.connect(self.chooseRect)
        self.actionEraser.triggered.connect(self.chooseEraser)
        self.actionOpen.triggered.connect(self.OpenImage)
        self.actionClear.triggered.connect(self.clear)
        self.actionInfo.triggered.connect(self.info)
        self.actionNew.triggered.connect(self.canvas.new)

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
        self.toolsmenu.addAction(self.actionSpray)
        self.toolsmenu.addAction(self.actionEraser)
        self.toolsmenu.addAction(self.actionClear)
        self.toolsmenu.addAction(self.actionNew)
        self.shapesmenu.addAction(self.actionLine)
        self.shapesmenu.addAction(self.actionCircle)
        self.shapesmenu.addAction(self.actionRect)
        self.helpmenu.addAction(self.actionInfo)

        self.toolbar.addAction(self.actionBrush)
        self.toolbar.addAction(self.actionEraser)
        self.toolbar.addAction(self.actionSpray)
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

#Работа с файлами
    def OpenImage(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open File', '',
            'Format (*.jpg);;Format (*.png)')[0]
        if fname != "":
            self.canvas.open(fname)

    def saveFile(self):
        fname = QFileDialog.getSaveFileName(
            self, 'Save file', '',
            'Format (*.jpg);;Format (*.png)')[0]
        if fname != "":
            self.canvas.currentImage.save(fname)

# Цвет кисти
    def color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_1.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.canvas.brushcolor = color

# Цвет заливки
    def color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_2.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.filloff.setText('FillON')
            self.filloff.setEnabled(True)
            self.canvas.fillcolor = color

    def setStartValues(self):
        self.button_1.setStyleSheet("background-color: white")
        self.button_2.setStyleSheet("background-color: white")
        self.filloff.setEnabled(False)
        self.SpinBoxBrushsize.setValue(1)
        self.lpx.setText('1px')

# Логика кнопок
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

    def info(self):
        message = '''* Правая кнопка мыши для вырезки\n* Левая кнопка мыши для рисования
* Слишком большие или слишком маленькие изображения могут некорректно открываться
* Приложение в стадии разработки, большинство функций отсутствует'''
        QMessageBox.information(self, 'Помощь', message,
            QMessageBox.Ok)

    def BrushSizeUpdate(self):
        self.canvas.brushsize = self.SpinBoxBrushsize.value()
        self.lpx.setText(f'{self.SpinBoxBrushsize.value()}px')

    def clear(self):
        self.canvas.currentImage.fill(QColor(255, 255, 255))
        self.canvas.update()

    def chooseBrush(self):
        self.canvas.instrument = 'Brush'

    def chooseSpray(self):
        self.canvas.instrument = 'Spray'

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
        ans = QMessageBox.question(
            self, 'Предупреждение!', message,
            QMessageBox.Save | QMessageBox.Close)
        if ans == QMessageBox.Close:
            QApplication.quit()
        elif ans == QMessageBox.Save:
            self.saveFile()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())