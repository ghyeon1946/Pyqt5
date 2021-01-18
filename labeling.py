import sys, os
import glob
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, QColorDialog, QGridLayout, QGraphicsScene, QComboBox, QMessageBox, QRadioButton, QTextEdit
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap, QColor, QPolygon
from PyQt5.QtCore import QPoint, QRect, Qt
from copy import deepcopy

data = {
    'dog': "red",
    'cat': 'blue'
}

# 그림은 QLabel에 QPixmap을 넣어서 만든다.
# QPixmap은 그냥 그림이라고 생각
class Canvas(QLabel):
    # Canvas 클래스를 생성할때 size를 받아서
    def __init__(self, parent, size):
        super().__init__(parent=parent)

        self.size = size
        self.setFixedSize(*size)

        self.begin = QPoint()
        self.end = QPoint()

        self.image_list = []
        self.boundBoxes = []
        self.image = None
        self.flag = False
        self.index = 0

        self.n = 'dog'


    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.flag = True
            self.begin = e.pos()
            self.end   = e.pos()
        elif e.buttons() == Qt.RightButton:
            print('right')
            self.removeBoundBox(e.pos())

    def removeBoundBox(self, pos):
        for boundBox in self.boundBoxes[::-1]:
            print(boundBox)
            x1, y1 = boundBox[0].x(), boundBox[0].y()
            x2, y2 = boundBox[1].x(), boundBox[1].y()

            if x1 <= pos.x() <= x2:
                if y1 <= pos.y() <= y2:
                    self.boundBoxes.remove(boundBox)
                    self.update()
                    break
                    
    def changeMouseMoveEvent2(self):
        self.n = 'dog'

    def changeMouseMoveEvent3(self):
        self.n = 'cat'

    def mouseMoveEvent(self, e):
        if self.flag == True:
            self.end = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.flag = False
            self.boundBoxes.append((self.begin, self.end, self.n))
            self.update()

    def ButtonClickedFile(self):
        self.fname = QFileDialog.getExistingDirectory()

        if self.fname:
            # QPixmap 객체
            self.image = None
            self.boundBoxes = []
            self.image_list = []
            self.index = 0
            self.image_list.extend(glob.glob(os.path.join(self.fname, "*.jpg")))
            self.image_list.extend(glob.glob(os.path.join(self.fname, "*.png")))
            
            self.init_widget()

    def paintEvent(self, event):
        if self.image == None:
            self.setPixmap(QPixmap())
            painter = QPainter(self)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRect(-100, -100, self.size[0]+100, self.size[1]+100)
            painter.end()
        else:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.image)

            for boundBox in self.boundBoxes:
                painter.setPen(QPen(QColor(data[boundBox[2]])))
                painter.drawRect(QRect(boundBox[0], boundBox[1]))

            if self.flag:
                painter.setPen(QPen(QColor(data[self.n])))
                painter.drawRect(QRect(self.begin, self.end))

            painter.end()
        
    def init_widget(self):
        if len(self.image_list) == 0:
            return
        
        self.image = QPixmap(self.image_list[0])
        self.loadFile()
        self.update()
        

    def preImage(self):
        if 0 == self.index:
            return

        self.saveFile()
        self.index -= 1 
        self.image = QPixmap(self.image_list[self.index])
        self.boundBoxes = []
        self.loadFile()
        self.update()

    def nextImage(self):
        if len(self.image_list) - 1 == self.index:
            return

        self.saveFile()
        self.index += 1 
        self.image = QPixmap(self.image_list[self.index])
        self.boundBoxes = []
        self.loadFile()
        self.update()

    def saveFile(self):
        txt_filename = self.get_text_filename()

        file = open(txt_filename, 'w')
        
        for index in range(len(self.boundBoxes)):
            # 0: 시작좌표 1: 끝좌표 2: 이름
            x1 = self.boundBoxes[index][0].x()
            y1 = self.boundBoxes[index][0].y()
            x2 = self.boundBoxes[index][1].x()
            y2 = self.boundBoxes[index][1].y()
            name = self.boundBoxes[index][2]
            line = '{},{},{},{},{}\n'.format(x1, y1, x2, y2, name)
            file.write(line)
        file.close()

    def loadFile(self):
        txt_filename = self.get_text_filename()

        if not os.path.isfile(txt_filename):
            self.boundBoxes = []
        else:
            file = open(txt_filename, 'r')
            for line in file.readlines():
                x1, y1, x2, y2, name = line.split(',')
                name = name.strip()
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                self.boundBoxes.append((QPoint(x1, y1), QPoint(x2, y2), name))
            file.close()

    def get_text_filename(self):
        image_path   = self.image_list[self.index]

        position     = image_path.rfind('.')          # 오른쪽 . 위치 찾기
        txt_filename = image_path[:position] + '.txt' # .txt 확장자 붙이기

        return txt_filename

    def close(self):
        self.saveFile()

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
        self.rbtn1.setChecked(True)
        self.rbtn1.clicked.connect(self.canvas.changeMouseMoveEvent2)

        self.rbtn2 = QRadioButton('Cat',self)
        self.rbtn2.move(880, 80)
        self.rbtn2.clicked.connect(self.canvas.changeMouseMoveEvent3)


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()