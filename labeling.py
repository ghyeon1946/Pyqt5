import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, QColorDialog, QGridLayout, QGraphicsScene, QComboBox, QMessageBox, QRadioButton, QTextEdit
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

        self.clear_canvas()

    def clear_canvas(self):
        painter = QPainter(self.pixmap())
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(-100, -100, self.size[0]+100, self.size[1]+100)
        painter.end()

    def Dog(self, e):
        if e.buttons() == Qt.LeftButton:
            t_pixmap = self.label1.pixmap()
            t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
            Square = QPainter(self.label1.pixmap())
            Square.setPen(QPen(QColor(255, 255, 255), 10))
            Square.drawRect(QRect(self.begin, e.pos()))
            Square.end()
            self.repaint()

    def Cat(self, e):
        if e.buttons() == Qt.LeftButton:
            t_pixmap = self.label1.pixmap()
            t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
            Square = QPainter(self.label1.pixmap())
            Square.setPen(QPen(QColor(255, 255, 255), 10))
            Square.drawRect(QRect(self.begin, e.pos()))
            Square.end()
            self.repaint()

    def mousePressEvent(self, e):
        self.begin = e.pos()
        self.update()

    def changeMouseMoveEvent2(self):
        self.mouseMoveEvent = self.Dog

    def changeMouseMoveEvent3(self):
        self.mouseMoveEvent = self.Cat

    def mouseMoveEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        Square = QPainter(self.label1.pixmap())
        Square.setPen(QPen(QColor(0, 0, 0), 10))
        Square.drawRect(QRect(self.begin, e.pos()))
        self.Pos = [self.begin, e.pos()]
        Square.end()
        self.repaint()

    def ButtonClickedFile(self):
        self.fname = QFileDialog.getExistingDirectory()

        if self.fname:
            # QPixmap 객체
            self.fname = os.path.realpath(self.fname)
            self.pixmap = [QPixmap(self.fname + '/' + self.img).scaled(800,620) for self.img in os.listdir(self.fname + '/')]

            self.pixmap[0] = self.pixmap[0].scaled(800,620)

            self.label1.setPixmap(self.pixmap[0])  # 이미지 세팅
            self.label1.resize(self.pixmap[0].width(), self.pixmap[0].height())

            self.show()

    def preImage(self):
        if self.cnt == 0:
                QMessageBox.about(self, "MESSAGE", "입력된 사진이 존재하지 않습니다.")
                pass

        else:
            self.cnt-=1
            if self.cnt == -1:
                QMessageBox.about(self, "MESSAGE", "첫번째 사진입니다.")
                pass

            self.label1.setPixmap(self.pixmap[self.cnt])
            self.saveFile()

    def nextImage(self):
        self.cnt+=1

        if self.cnt == 1:
                QMessageBox.about(self, "MESSAGE", "입력된 사진이 존재하지 않습니다.")
                pass

        else:
            if self.cnt == len(self.pixmap):
                QMessageBox.about(self, "MESSAGE", "마지막 사진입니다.")
                self.cnt=0

            self.label1.setPixmap(self.pixmap[self.cnt])
            self.saveFile()

    def saveFile(self):
        #self.FileSave = QFileDialog.getSaveFileName(self, "Save file", "", "Text files (*.txt)")
        self.file = open(self.img +'.txt','w')
        if self.Pos[0]:
            self.file.write("("+str(self.Pos[0].x()) +","+ str(self.Pos[0].y()) + ")"  
            + " " + "("+str(self.Pos[1].x()) +","+ str(self.Pos[1].y()) + ")")
        self.file.close()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas(self, (850, 620))
        self.canvas.move(30, 30)
        self.setFixedSize(1000, 720)
        self.canvas.move(10, 10)

        self.canvas.setCursor(Qt.CrossCursor)

        self.init_UI()
        self.show()

    def init_UI(self):
        self.backbtn = QPushButton('디렉터리 선택', self)
        self.backbtn.resize(110, 50)
        self.backbtn.move(20, 640)
        self.backbtn.clicked.connect(self.canvas.ButtonClickedFile)

        self.prebtn = QPushButton('<', self)
        self.prebtn.resize(110, 50)
        self.prebtn.move(730, 640)
        self.prebtn.clicked.connect(self.canvas.preImage)

        self.nextbtn = QPushButton('>', self)
        self.nextbtn.resize(110, 50)
        self.nextbtn.move(850, 640)
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