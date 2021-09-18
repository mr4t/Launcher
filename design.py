from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import os
box_x = 78
box_y = 150
box_l = {}
# styles
but_style = ("QPushButton::pressed{"
             "background-color:black;"
             "border-color:red;}"
             "QPushButton{"
             "border-radius:6px;"
             "border-width: 1px;"
             "border-style:outset;"
             " border-color: blue;"
             "background-color:rgba(0, 0, 0, 0);; "
             " color: white;}")
line_style = ("QLineEdit::focus{"
              "background-color:rgba(0, 0, 0, 0);;"
              "border-color: red;}"
              "QLineEdit{"
              "border-radius:6px;"
              "border-width: 1px;"
              "border-style:outset;"
              "border-color: blue;"
              "background-color:rgba(0, 0, 0, 0);; "
              "color: white;}")


def textbox(obj, lx, ly, sx, sy, placeholder="", completer=[]):
    obj.setPlaceholderText(placeholder)
    obj.move(lx, ly)
    obj.resize(sx, sy)
    obj.setStyleSheet(line_style)
    obj.setCompleter(QCompleter(completer))


def label(obj, lx, ly, sx, sy, text, stat):
    obj.setAlignment(Qt.AlignCenter)
    obj.resize(sx, sy)
    obj.setText(text)
    obj.move(lx, ly)
    obj.setStyleSheet("color :" + stat + ";")


def classicBut(obj, lx, ly, sx, sy):
    obj.move(lx, ly)
    obj.resize(sx, sy)
    obj.setStyleSheet(but_style)


def classicLine(obj, lx, ly, sx, sy, placeholder=""):
    obj.setPlaceholderText(placeholder)
    obj.move(lx, ly)
    obj.resize(sx, sy)
    obj.setStyleSheet(line_style)


def appBoxes(objBut, objLine, db_data):
    global box_x
    global box_y
    if os.path.exists(db_data[2]):
        objBut.setIcon(QIcon(db_data[2]))
    else:
        objBut.setIcon(QIcon("logo/image-not-foundW.png"))
    objBut.setIconSize(QSize(60, 60))
    objBut.setFixedSize(60, 60)
    objBut.move(box_x, box_y)
    # objBut.installEventFilter(parent)
    objBut.setStyleSheet("QPushButton{"
                         "border-style:outset;"
                         "border-color: blue;"
                         "color: white;}")

    objLine.setText(db_data[0])
    objLine.setStyleSheet("color :white;")
    objLine.resize(70, 20)
    objLine.move(box_x - 5, box_y + 70)
    objLine.setAlignment(Qt.AlignCenter)
    # box_x += 86
    # box_y +=
    # 70 + 86*x + 70 = 1000 x=10
    box_l[objBut] = [box_x, box_y]
    if box_x + 86 > 860:
        box_x = 78
        box_y += 100
    else:
        box_x += 86


def appBoxesHoverOk(obj):
    obj.setIconSize(QSize(60, 60))
    obj.setFixedSize(60, 60)
    obj.move(box_l[obj][0], box_l[obj][1])
    obj.setStyleSheet("QPushButton{"
                      "border-style:outset;"
                      "border-color: blue;"
                      "color: white;}")


def appBoxesOnHovered(obj):
    obj.setIconSize(QSize(70, 70))
    obj.setFixedSize(70, 70)
    obj.move(box_l[obj][0] - 5, box_l[obj][1] - 5)
    obj.setStyleSheet("QPushButton{"
                      "border-style: outset;"
                      "border-color: blue;"
                      "color: white;}")
