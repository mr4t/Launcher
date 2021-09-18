import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFrame, QVBoxLayout ,QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPainter, QPen
import design
from title_bar_settings import MyBar
from db_manager import manage
import os
class settings(QWidget):
    def __init__(self):
        super(settings, self).__init__()
        self.manage = manage(self, "apps.db")
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # title bar tanımları
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyBar(self))  # set mybar
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(-1)
        self.pressing = False

        # title bar ile window ayrımı (split line)
        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 30, 800, 3))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setStyleSheet("color:#616161")

        # set bg
        self.setBG()

        # set name
        self.name = QLineEdit(self)
        design.classicLine(self.name, 50, 50, 700, 40, "Set App Name")

        # uygulama yolu
        self.appPathText = QLineEdit(self)
        design.classicLine(self.appPathText, 50, 110, 620, 40, "Set Path for App")

        # uygulama ekleme butonu
        self.appPathBut = QPushButton("Browse", self)
        design.classicBut(self.appPathBut, 675, 110, 75, 40)

        # icon yolu
        self.iconPathText = QLineEdit(self)
        design.classicLine(self.iconPathText, 50, 170, 620, 40, "Set Path for Icon")

        # icon ekleme butonu
        self.iconPathBut = QPushButton("Browse", self)
        design.classicBut(self.iconPathBut, 675, 170, 75, 40)

        # ekle butonu
        self.addApp = QPushButton("Add App", self)
        design.classicBut(self.addApp, 50, 230, 100, 35)

        # silinecek dosya adı
        self.deleteText = QLineEdit(self)
        design.classicLine(self.deleteText, 50, 360, 620, 40, "Silinecek dosya adı")

        # silme butonu
        self.deleteBut = QPushButton("DELETE", self)
        design.classicBut(self.deleteBut, 675, 360, 75, 40)

        self.appPathBut.clicked.connect(self.appBrowser)
        self.iconPathBut.clicked.connect(self.iconBrowser)
        self.addApp.clicked.connect(self.addDB)
        self.deleteBut.clicked.connect(self.delDB)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())
    def delDB(self):
        self.manage.remove(self.deleteText.text().strip())

    def addDB(self):
        if len(self.name.text().strip()) < 12:
            self.manage.append(self.name.text().strip(), self.appPathText.text().strip(), self.iconPathText.text().strip())
        else:
            box = QMessageBox()
            self.manage.message(box, QMessageBox.Warning, "isim bilgisi 12 karkterden kısa olmalıdır.")

    def appBrowser(self):
        self.home_dir = os.path.expanduser("~")
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', self.home_dir)
        self.appPathText.setText(self.fname[0])

    def iconBrowser(self):
        self.home_dir = os.path.expanduser("~")
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', self.home_dir)
        self.iconPathText.setText(self.fname[0])

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = settings()
    sys.exit(app.exec_())