import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, QColorDialog, QGridLayout, QGraphicsScene, QComboBox, QMessageBox, QRadioButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap, QColor, QPolygon
from PyQt5.QtCore import QPoint, QRect, Qt
from copy import deepcopy

# 그림은 QLabel에 QPixmap을 넣어서 만든다.
# QPixmap은 그냥 그림이라고 생각
class Canvas(QLabel):
    # Canvas 클래스를 생성할때 size를 받아서
    def __init__(self, parent, size):
        super().__init__(parent=parent)

        self.size = size
        self.setPixmap(QPixmap(*size))
        self.setFixedSize(*size)

        self.label1 = QLabel(self)
        self.label1.move(0, 0)

        self.begin = QPoint()
        self.end = QPoint()

        self.cnt = 0
        self.path = ['사진 경로                                                  ']

        self.clear_canvas()

    def clear_canvas(self):
        painter = QPainter(self.pixmap())
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(-100, -100, self.size[0]+100, self.size[1]+100)
        painter.end()

    # def Dog(self, e):
    #     t_pixmap = self.pixmap()
    #     t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
    #     Square = QPainter(self.pixmap())
    #     Square.setPen(QPen(QColor(100, 100, 100), 10))
    #     Square.drawRect(QRect(self.begin, e.pos()))
    #     Square.end()
    #     self.repaint()
    #     self.setPixmap(t_pixmap)
  
    def Dog(self, e):
        if e.buttons() == Qt.LeftButton:
            painter = QPainter(self.pixmap())
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            # painter.drawPixmap(self.rect(), imagePixmap)
            painter.drawRect(QRect(self.begin, e.pos()))
            painter.end()
            self.update()
            # self.repaint()
    
    def Cat(self, e):
        t_pixmap = self.pixmap()
        t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
        Square = QPainter(self.pixmap())
        Square.setPen(QPen(QColor(0, 0, 0), 10))
        Square.drawRect(QRect(self.begin, e.pos()))
        Square.end()
        self.repaint()
        self.setPixmap(t_pixmap)

    def mousePressEvent(self, e):
        self.begin = e.pos()
        self.update()

    def changeMouseMoveEvent2(self):
        print('hi')
        self.mouseMoveEvent = self.Dog

    def changeMouseMoveEvent3(self):
        self.mouseMoveEvent = self.Cat

    def mouseMoveEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        Square = QPainter(self.pixmap())
        Square.setPen(QPen(QColor(0, 0, 0), 10))
        Square.drawRect(QRect(self.begin, e.pos()))
        Square.end()
        self.repaint()

    def ButtonClickedFile(self):
        fname = QFileDialog.getOpenFileName()

        if fname[0]:
            # QPixmap 객체
            self.cnt = self.cnt + 1
            self.path.append(fname[0])

            pixmap = QPixmap.fromImage(fname[0])
            print(self.path[self.cnt])

            MainWindow.setLabel(self.path, self.cnt)

            self.label1.setPixmap(pixmap)  # 이미지 세팅
            self.label1.resize(pixmap.width(), pixmap.height())

            # 이미지의 크기에 맞게 Resize
            self.resize(pixmap.width(), pixmap.height())

            # self.show()

    def preImage(self):
        pass

    def nextImage(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas(self, (850, 620))
        self.setFixedSize(1000, 720)
        
        self.setCentralWidget(self.canvas)
        self.init_UI()
        self.show()

    def init_UI(self):
        self.backbtn = QPushButton('디렉터리 선택', self)
        self.backbtn.resize(110, 50)
        self.backbtn.move(20, 630)
        self.backbtn.clicked.connect(self.canvas.ButtonClickedFile)

        self.prebtn = QPushButton('<', self)
        self.prebtn.resize(110, 50)
        self.prebtn.move(730, 630)
        self.prebtn.clicked.connect(self.canvas.preImage)

        self.nextbtn = QPushButton('>', self)
        self.nextbtn.resize(110, 50)
        self.nextbtn.move(850, 630)
        self.nextbtn.clicked.connect(self.canvas.nextImage)

        self.rbtn1 = QRadioButton('Dog',self)
        self.rbtn1.move(880, 50)
        self.rbtn1.clicked.connect(self.canvas.changeMouseMoveEvent2)

        self.rbtn2 = QRadioButton('Cat',self)
        self.rbtn2.move(880, 80)
        self.rbtn2.clicked.connect(self.canvas.changeMouseMoveEvent3)

    def setLabel(self, path, num):
        self.label1.setText(path[num])


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    app.exec_()