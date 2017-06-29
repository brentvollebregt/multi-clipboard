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

def clear(clipboards_location, clipboard):
    extension = bmpOrTxt(clipboards_location + clipboard)
    if extension:
        os.remove(clipboards_location + clipboard + extension)
        return True
    else:
        return False

def view_single(clipboards_location, clipboard):
    extension = bmpOrTxt(clipboards_location + clipboard)
    if extension == '.bmp':
        image = Image.open(clipboards_location + sys.argv[2] + ".bmp")
        image.show()
        print ("Image displayed")
        return True
    elif extension == '.txt':
        print ("Clipboard text:")
        f = open(clipboards_location + sys.argv[2] + ".txt", 'r')
        print (f.read())
        f.close()
        return True
    else:
        return False

def view(clipboards_location):
    app = QtWidgets.QApplication(sys.argv)
    # print (app.desktop().screenGeometry().width(), app.desktop().screenGeometry().height())
    # print (QtWidgets.QDesktopWidget().screenGeometry(-1))
    # print (app.primaryScreen().size().width(), app.primaryScreen().size().height())
    MainWindow = QtWidgets.QMainWindow()
    prog = GUIObject(MainWindow, clipboards_location)
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

def bmpOrTxt(base):
    if os.path.isfile(base + ".bmp"):
        return '.bmp'
    elif os.path.isfile(base + ".txt"):
        return '.txt'
    else:
        return False

class GUIObject(GUI.Ui_MainWindow):
    def __init__(self, MainWindow, clipboards_location):
        GUI.Ui_MainWindow.__init__(self)
        self.setupUi(MainWindow)
        self.MW = MainWindow
        self.clipboards_location = clipboards_location
        MainWindow.setWindowOpacity(0.85)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setFixedSize(MainWindow.frameGeometry().width(), MainWindow.frameGeometry().height())

        icon = QtGui.QPixmap('images/close.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_9.setPixmap(icon)
        self.label_9.mousePressEvent = self.closeButton

        icon = QtGui.QPixmap('images/delete.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_8.setPixmap(icon)
        self.label_8.mousePressEvent = self.deleteButton

        icon = QtGui.QPixmap('images/refresh.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_7.setPixmap(icon)
        self.label_7.mousePressEvent = self.refreshButton

        icon = QtGui.QPixmap('images/add.png')
        icon = icon.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        self.label_6.setPixmap(icon)
        self.label_6.mousePressEvent = self.addButton


        self.clipboards = []
        for item in os.listdir(self.clipboards_location):
            if item.endswith('.bmp') or item.endswith('.png'):
                self.clipboards.append(item)

        # TODO Display each label
        # Size them
        # Size window


    def closeButton(self, event):
                self.MW.close()

    def deleteButton(self, event):
        reply = QtWidgets.QMessageBox.warning(self.MW,
                                              'Warning',
                                              "You are about to clear all clipboards.\nDo you want to proceed?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            print ("Delete")

    def addButton(self, event):
        print ("Add")

    def refreshButton(self, event):
        print ("Refresh")

    def labelClickEvent(self, event):
        widgets = self.centralwidget.children()
        for widget in widgets:
            hasGeo = getattr(widget, "mapToGlobal", None)
            if not callable(hasGeo):
                continue
            if widget.mapToGlobal(event.pos()) == event.globalPos():
                print (widget.objectName())
