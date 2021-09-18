# pyqt5 5.9.2
# python 3.8.5
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton, QMessageBox)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QPainter, QPen
import os
from title_bar import MyBar
import design
from db_manager import manage

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Launcher'
        self.fill_name = []
        self.manage = manage(self, "apps.db")
        self.j = 0
        self.setWindowIcon(QIcon("logo/icon.ico"))
        self.initUI()

    def initUI(self):
        for i in self.manage.read():
            self.fill_name.append(i[0])
        # genel pencere özellikleri
        self.setWindowTitle(self.title)
        self.setFixedSize(1000, 800)
        self.error = QLabel(self)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # title bar tanımları
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))  # set mybar
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)

        # title bar ile window ayrımı (split line)
        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 30, 1000, 3))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setStyleSheet("color:#616161")

        # set bg
        self.setBG()

        # textbox
        self.textbox = QLineEdit(self)
        design.textbox(self.textbox, 300, 50, 400, 30, "App Name", self.fill_name)
        design.box_x = 78
        design.box_y = 150

        for i in self.manage.read():
            exec("self.but"+str(self.j)+" = QPushButton(self, objectName = '" + i[0] + "')")
            exec("self.line"+str(self.j)+" = QLabel(self)")
            exec("design.appBoxes(self.but"+str(self.j)+", self.line"+str(self.j)+", i)")
            exec("self.but"+str(self.j)+".installEventFilter(self)")

        self.show()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.runAppText()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton:
            self.ver = True
        elif event.type() == QtCore.QEvent.MouseButtonRelease and self.ver:
            self.ver = False
            self.runAppBut(obj.objectName())
        if event.type() == QtCore.QEvent.HoverEnter:
            design.appBoxesOnHovered(obj)
        elif event.type() == QtCore.QEvent.HoverLeave:
            design.appBoxesHoverOk(obj)
        return super(App, self).eventFilter(obj, event)

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
                box = QMessageBox()
                self.manage.message(box, QMessageBox.Warning, "Arkaplan resmi bulunamadı.\nVarsayılan ayarlar gösteriliyor.")
                self.setStyleSheet("background-color: #2f2f2f;")
        else:
            self.setStyleSheet("background-color: "+data[2]+";")


    def runAppBut(self, name):
        ver = True
        data = self.manage.read()
        for i in data:
            if name == i[0]:
                data = i
                ver = False
                break
        if ver:
            design.label(self.error, 435, 100, 160, 20, "Uygulama Başlatılamadı", "red")
        else:
            try:
                os.startfile(str(data[1]))
                design.label(self.error, 435, 100, 130, 20, "Uygulama Başladı", "green")
            except:
                design.label(self.error, 435, 100, 160, 20, "Uygulama Başlatılamadı", "red")

    def runAppText(self):
        ver = True
        data = self.manage.read()
        for i in data:
            if self.textbox.text().strip() == i[0]:
                data = i
                ver = False
                break
        if ver:
            design.label(self.error, 435, 100, 130, 20, "Uygulama Bulunamadı", "red")
        else:
            os.startfile(str(data[1]))
            design.label(self.error, 435, 100, 130, 20, "Uygulama Başladı", "green")

    def but(self, name, lx, ly, sx, sy, style):
        name.move(lx, ly)
        name.resize(sx, sy)
        self.but1.setStyleSheet(style)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
