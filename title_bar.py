from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
import settings
from background import background
class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("LAUNCHER")
        self.btn_size = 30

        self.quit = QPushButton("X")
        self.quit.clicked.connect(self.btn_close_clicked)
        self.quit.setFixedSize(self.btn_size+10, self.btn_size)
        self.quit.setStyleSheet("QPushButton::hover{"
                                "background-color:red;}"
                                "QPushButton::pressed{"
                                "background-color:#FF7676;}"
                                "QPushButton{"
                                "border-style:outset;"
                                "border-color: blue;"
                                "color: white;}")

        self.minimize = QPushButton("-")
        self.minimize.clicked.connect(self.btn_min_clicked)
        self.minimize.setFixedSize(self.btn_size+10, self.btn_size)
        self.minimize.setStyleSheet("QPushButton::hover{"
                                    "background-color:gray;}"
                                    "QPushButton{"
                                    "border-style:outset;"
                                    "border-color: blue;"
                                    "color: white;}")

        self.background = QPushButton()
        self.background.setIcon(QIcon("logo/sunsetW.png"))
        self.background.clicked.connect(background)
        self.background.setFixedSize(self.btn_size + 10, self.btn_size)
        self.background.setStyleSheet("QPushButton::hover{"
                                    "background-color:gray;}"
                                    "QPushButton{"
                                    "border-style:outset;"
                                    "border-color: blue;"
                                    "color: white;}")

        self.settings = QPushButton()
        self.settings.setIcon(QIcon("logo/settingsW.png"))
        self.settings.clicked.connect(settings.settings)
        self.settings.setFixedSize(self.btn_size + 10, self.btn_size)
        self.settings.setStyleSheet("QPushButton::hover{"
                                      "background-color:gray;}"
                                      "QPushButton{"
                                      "border-style:outset;"
                                      "border-color: blue;"
                                      "color: white;}")


        self.title.setStyleSheet("color :white; padding-left:10px;")

        self.layout.addWidget(self.background)
        self.layout.addWidget(self.settings)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minimize)
        self.layout.addWidget(self.quit)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
#-----------------------------------------------------------ARAYUZ

    def pr(self):
        print("ok")

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()
