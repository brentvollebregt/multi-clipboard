import win32clipboard
from PIL import ImageGrab, Image
from io import BytesIO
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import GUI
import logging
import os
import shutil
import json

def saveClipboard(clipboards_location, data):
    if not os.path.exists(clipboards_location):
        os.makedirs(clipboards_location)
    try:
        win32clipboard.OpenClipboard()
        current_clipboard_text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        f = open(clipboards_location + data["current_clipboard"] + ".txt", 'w')
        f.write(current_clipboard_text)
        f.close()

        if os.path.isfile(clipboards_location + data["current_clipboard"] + ".bmp"):
            os.remove(clipboards_location + data["current_clipboard"] + ".bmp")
    except TypeError:
        try:
            im = ImageGrab.grabclipboard()
            im.save(clipboards_location + data["current_clipboard"] + ".bmp", 'BMP')

            if os.path.isfile(clipboards_location + data["current_clipboard"] + ".txt"):
                os.remove(clipboards_location + data["current_clipboard"] + ".txt")
        except:
            print ("Clipbaord contents not supported")
            return False
    except Exception as e:
        print ("Unexpected error")
        print (e)
        return False
    return True

def loadClipboard(clipboards_location, clipboard):
    if os.path.isfile(clipboards_location + clipboard + ".bmp"):
        image = Image.open(clipboards_location + clipboard + ".bmp")
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        clipboard_data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, clipboard_data)
        win32clipboard.CloseClipboard()
        pass
    elif os.path.isfile(clipboards_location + clipboard + ".txt"):
        f = open(clipboards_location + clipboard + ".txt")
        clipboard_data = f.read()
        f.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(clipboard_data)
        win32clipboard.CloseClipboard()

def clear():
    pass

def view(clipboard):
    pass

def view():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    prog = GUIObject(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def getData():
    with open('data.json') as data_file:
        return json.load(data_file)

def setData(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    return True

def cleanString(string):
    # Thanks to https://stackoverflow.com/questions/7406102/create-sane-safe-filename-from-any-unsafe-string
    keepcharacters = ('.', '_', '[', ']', '(', ')')
    string = "".join(c for c in string if c.isalnum() or c in keepcharacters).rstrip()
    return string

class GUIObject(GUI.Ui_MainWindow):
    def __init__(self, MainWindow):
        GUI.Ui_MainWindow.__init__(self)
        self.setupUi(MainWindow)
        self.MW = MainWindow
        MainWindow.setWindowOpacity(0.85)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setFixedSize(MainWindow.frameGeometry().width(), MainWindow.frameGeometry().height())

        icon = QtGui.QPixmap('images/close.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_8.setPixmap(icon)
        clickable(self.label_8).connect(self.closeButton)

        icon = QtGui.QPixmap('images/delete.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_9.setPixmap(icon)

        icon = QtGui.QPixmap('images/refresh.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_7.setPixmap(icon)

        icon = QtGui.QPixmap('images/add.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_6.setPixmap(icon)

    def closeButton(self):
        print ("Close")
        self.MW.close()

    def deleteButton(self):
        print ("Delete")

    def addButton(self):
        print ("Add")

    def keyPressEvent(self):
        print ("some key")

def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
