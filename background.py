from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QColorDialog,
                             QVBoxLayout, QFrame, QFileDialog, QLabel, QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QPainter, QPen
import design
from db_manager import manage
from title_bar_settings import MyBar
import os

class background(QWidget):

    def __init__(self):
        super(background, self).__init__()
        self.manage = manage(self, "apps.db")
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))  # set mybar
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.pressing = False

        # title bar ile window ayrımı (split line)
        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 29, 500, 1))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setStyleSheet("color:#616161")

        self.changeColor = QPushButton("Renk Seç", self)
        self.changeColor.clicked.connect(self.colorPreview)
        self.changeColor.move(20, 50)
        self.changeColor.resize(370, 30)
        self.changeColor.setStyleSheet("color : white; background-color:black;")

        self.colorBut = QPushButton("Ayarla", self, objectName= "colorBut")
        design.classicBut(self.colorBut, 400, 50, 80, 30)
        self.colorBut.installEventFilter(self)

        self.imageText = QLineEdit(self)
        design.textbox(self.imageText, 20, 100, 280, 30, "arkaplan resim yolu")

        self.pathBut = QPushButton("Resim Seç", self)
        design.classicBut(self.pathBut,310, 100, 80, 30)
        self.pathBut.clicked.connect(self.browser)

        self.imageBut = QPushButton("Ayarla", self, objectName= "imageBut")
        design.classicBut(self.imageBut, 400, 100, 80, 30)
        self.imageBut.installEventFilter(self)

        self.bgColor = QLabel("color preview", self)
        self.bgColor.setAlignment(Qt.AlignTop)
        self.bgColor.move(20, 170)
        self.bgColor.setFixedSize(200,200)
        self.bgColor.setStyleSheet("color: white;")

        self.bgImage = QLabel("image preview", self)
        self.bgImage.setAlignment(Qt.AlignTop)
        self.bgImage.move(260, 170)
        self.bgImage.setFixedSize(200, 200)
        self.bgImage.setStyleSheet("color: white;")
        self.setBG()
        self.show()
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton:
            if obj.objectName() == "imageBut":
                self.manage.changeBG(obj.objectName(), self.imageText.text().strip())
            else:
                try:
                    self.manage.changeBG(obj.objectName(), self.color.name())
                except:
                    self.manage.changeBG(obj.objectName(), "black")

        return super(background, self).eventFilter(obj, event)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())

    def setBG(self):
        data = self.manage.setBG()
        if data[1] == "imageBut":
            if os.path.exists(data[2]):
                oImage = QImage(data[2])
                sImage = oImage.scaled(QSize(self.width(), self.height()))
                palette = QPalette()
                palette.setBrush(QPalette.Window, QBrush(sImage))
                self.setPalette(palette)
            else:
                self.setStyleSheet("background-color: #2f2f2f;")
        else:
            self.setStyleSheet("background-color: " + data[2] + ";")

    def colorPreview(self):
        self.color = QColorDialog.getColor()
        try:
            self.changeColor.setStyleSheet("background-color :" + self.color.name() + ";"
                                            "border-style :outset;"
                                           "color: white;")
            self.bgColor.setStyleSheet("color: white; background-color :" + self.color.name() + ";")
            self.bgColor.setText("")
        except:
            self.changeColor.setStyleSheet("background-color :black;"
                                          "border-style :outset;"
                                          "color: white;")
            self.bgColor.setStyleSheet("color: white; background-color :black;")
            self.bgColor.setText("")
        # print(color.name())

    def browser(self):
        self.home_dir = os.path.expanduser("~")
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', self.home_dir)
        self.imageText.setText(self.fname[0])

        pixmap = QPixmap(self.fname[0])
        self.bgImage.setPixmap(pixmap)
        self.bgImage.setScaledContents(True)

