from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import sqlite3 as lite
import os
class manage():
    def __init__(self,parent, name):
        super(manage, self).__init__()
        self.parent = parent
        self.name = name
        self.db = lite.connect(self.name)
        self.createTable()

    def createTable(self):
        self.im = self.db.cursor()
        self.im.execute(r"CREATE TABLE IF NOT EXISTS launcher ('app_name', 'app_path', 'icon_path')")
        self.im.execute(r"CREATE TABLE IF NOT EXISTS color ('num', 'button', 'color')")
        self.db.commit()

    def setBG(self):
        self.im = self.db.cursor()
        self.im.execute("SELECT * FROM color")
        try :
            return self.im.fetchall()[0]
        except:
            return [0, "colorBut", "#2F2F2F"]

    def changeBG(self, button, bg):
        num = 0
        try:
            self.im.execute('DELETE FROM color WHERE num=?', (num,))
        except:
            pass
        if button == "colorBut":
            self.im = self.db.cursor()
            self.im.execute("INSERT INTO color VALUES (?,?,?)", (num, button, bg))
            self.db.commit()
            box = QMessageBox()
            self.message(box, QMessageBox.Information, "Arkaplan ayarlandı.\nDeğişikliler uygulama yeniden başlayınca uygulanacak")

        elif button == "imageBut":
            if not os.path.exists(bg):
                box = QMessageBox()
                self.message(box, QMessageBox.Warning, "Error!!!\nResim için doğru yolu verdiğinizden emin olun.")
            else:
                if not os.path.splitext(bg)[1] in [".png", ".jpg", ".jpeg", ".ico"]:
                    box = QMessageBox()
                    self.message(box, QMessageBox.Warning, "Error!!!\nDesteklenmeyen dosya tipi.")
                else:
                    self.im = self.db.cursor()
                    os.system('copy "' + "\\".join((bg.split("/"))) + '" "logo\\background'+os.path.splitext(bg)[1])
                    self.im.execute("INSERT INTO color VALUES (?,?,?)", (num, button, "logo/background" + os.path.splitext(bg)[1]))
                    self.db.commit()
                    box = QMessageBox()
                    self.message(box, QMessageBox.Information, "Arkaplan ayarlandı.\nDeğişikliler uygulama yeniden başlayınca uygulanacak")

    def read(self):
        self.im = self.db.cursor()
        self.im.execute("SELECT * FROM launcher")
        return self.im.fetchall()

    def append(self, app_name, app_path, icon_path):
        data = self.read()
        ver = True
        for i in data:
            if app_name == i[0]:
                # print("belirtilen isim daha önce kullanılmış")
                box = QMessageBox()
                self.message(box, QMessageBox.Warning, "Belirtilen isim daha önce kullanılmış.")
                ver = False
                break

        if ver and (not os.path.exists(app_path) or ((not os.path.exists(icon_path)) and icon_path != "") or app_name == ""):
            # print("Error\nLütfen girdileri kontrol edin hepsinin dolduruluduğundan ve doğru yolu verdiğinizden emin olun")
            box = QMessageBox()
            self.message(box, QMessageBox.Warning, "Error!!!\nLütfen girdileri kontrol edin.\nHepsinin doldurulduğundan ve doğru yolları verdiğinizden emin olun.")
            ver = False
        if ver:
            self.im = self.db.cursor()

            self.im.execute("INSERT INTO launcher VALUES (?,?,?)", (app_name, app_path, "icons/"+app_name+os.path.splitext(icon_path)[1] ))
            self.db.commit()
            box = QMessageBox()
            # print("Ugulama Eklendi")
            self.message(box, QMessageBox.Information, "Uygulama Eklendi.\n"+app_name)
            os.system('copy "' + "\\".join((icon_path.split("/"))) + '" "icons\\'+app_name + os.path.splitext(icon_path)[1])


    def remove(self, name):
        self.im = self.db.cursor()
        data = self.read()
        ver = False
        for i in data:
            if name == i[0]:
                ver = True
                break
        if ver:
            self.im.execute('DELETE FROM launcher WHERE app_name=?', (name,))  # uygulamayı kaldır
            data = self.read()
            for i in data:
                if name == i[0]:
                    ver = False
            if not ver:
                # print("Silme işlemi başarısız")
                box = QMessageBox()
                self.message(box, QMessageBox.Warning, "Silme İşlemi Başarısız")
            else:
                # print("Silme işlemi şu uygulama için tamamlandı :" + name)
                box = QMessageBox()
                self.message(box, QMessageBox.Information, "Silme işlemi şu uygulama için tamamlandı :" + name)
                os.system('del /f "icons\\'+name+'.*"')
        else:
            # print("Uygulama bulunamadı")
            box = QMessageBox()
            self.message(box, QMessageBox.Warning, "Uygulama Bulunamadı")
        self.db.commit()

    def message(self, box, icon, description):
        box.setWindowFlag(Qt.WindowStaysOnTopHint)
        box.setText(description)
        box.setIcon(icon)
        box.setWindowTitle("LAUNCHER")
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()
