import win32clipboard
from PIL import ImageGrab, Image
from io import BytesIO
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import GUI
import os
import json
from ast import literal_eval
import subprocess

def saveClipboard(clipboards_location, data):
    if not os.path.exists(clipboards_location):
        os.makedirs(clipboards_location)
    try:
        win32clipboard.OpenClipboard()

        # Check if the clipboard contains a list of file references
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            current_clipboard = list(win32clipboard.GetClipboardData(win32clipboard.CF_HDROP))
            win32clipboard.CloseClipboard()

            f = open(clipboards_location + data["current_clipboard"] + ".txt", 'w')
            f.write("FILE\n")
            f.write(str(current_clipboard))
            f.close()

            if os.path.isfile(clipboards_location + data["current_clipboard"] + ".bmp"):
                os.remove(clipboards_location + data["current_clipboard"] + ".bmp")

        # Otherwise, treat it as text and let the normal exceptions handle the rest
        elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
            current_clipboard = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f = open(clipboards_location + data["current_clipboard"] + ".txt", 'w')
            f.write("TEXT\n")
            f.write(current_clipboard)
            f.close()

            if os.path.isfile(clipboards_location + data["current_clipboard"] + ".bmp"):
                os.remove(clipboards_location + data["current_clipboard"] + ".bmp")
        # Image
        elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_BITMAP):
            im = ImageGrab.grabclipboard()
            im.save(clipboards_location + data["current_clipboard"] + ".bmp", 'BMP')

            if os.path.isfile(clipboards_location + data["current_clipboard"] + ".txt"):
                os.remove(clipboards_location + data["current_clipboard"] + ".txt")
        # Something other than text, file(s) or image data
        else:
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
        data_type = f.readline().strip()
        # Read the type of data
        if data_type == "FILE":
            # Set the file data using powershell commands as its much easier, and fits majority of use cases
            clipboard_data = "(" + f.read()[1:-1] + ")"
            subprocess.call(["powershell.exe", "Set-Clipboard -Path " + clipboard_data])
        # Assume text if nothing else
        else:
            clipboard_data = f.read()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(clipboard_data)
            win32clipboard.CloseClipboard()

        f.close()

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
        image = Image.open(clipboards_location + clipboard + ".bmp")
        image.show()
        return True
    elif extension == '.txt':
        f = open(clipboards_location + clipboard + ".txt", 'r')
        print (f.read())
        f.close()
        return True
    else:
        return False

def view(clipboards_location):
    app = QtWidgets.QApplication(sys.argv)
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
    def __init__(self, MainWindow, clipboards_location, initial=True):
        GUI.Ui_MainWindow.__init__(self)
        self.MW = MainWindow
        self.setupUi(self.MW)
        self.clipboards_location = clipboards_location
        self.MW.setWindowOpacity(0.85)
        if initial:
            self.MW.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        saveClipboard(self.clipboards_location, getData())

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
            if item.endswith('.bmp') or item.endswith('.txt'):
                self.clipboards.append(item)
        self.clipboards = self.clipboards[::-1] # Reverse for pop

        if len(self.clipboards) <= 5:
            level = 1
        else:
            clipboard_amount = len(self.clipboards) - 5
            level = 1 + int(clipboard_amount / 6)
            if clipboard_amount % 6 != 0:
                level += 1

        self.clipboard_labels = {}
        labels = 0
        if level == 1:
            for i in range(len(self.clipboards)):
                labels = self.createLabel(labels, (10 + (140 * labels)), 10)

            self.label_6.setGeometry(QtCore.QRect((10 + (140 * labels)), 10, 61, 61))
            self.label_7.setGeometry(QtCore.QRect((80 + (140 * labels)), 10, 61, 61))
            self.label_8.setGeometry(QtCore.QRect((10 + (140 * labels)), 80, 61, 61))
            self.label_9.setGeometry(QtCore.QRect((80 + (140 * labels)), 80, 61, 61))
            self.MW.resize((151 + (140 * labels)), 151)
        else:
            for i in range(5):
                labels = self.createLabel(labels, (10 + (140 * labels)), 10)
            for current_mid_level in range(level - 2):
                for i in range(6):
                    labels = self.createLabel(labels, (10 + (140 * (labels - 5 - (current_mid_level * 6)))), (10 + (140 * (current_mid_level + 1))))
            for i in range(len(self.clipboards)):
                labels = self.createLabel(labels, (10 + (140 * (labels - 5 - ((level - 2) * 6)))), (10 + (140 * (level - 1))))

            self.MW.resize(851 , (10 + (140 * level)))

    def createLabel(self, labels, x, y):
        tmp = self.clipboards.pop()
        self.clipboard_labels[labels] = QtWidgets.QLabel(self.centralwidget)
        self.clipboard_labels[labels].setGeometry(QtCore.QRect(x, y, 131, 131))
        self.clipboard_labels[labels].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        data = getData()
        if data["current_clipboard"] == tmp[:-4]:
            self.clipboard_labels[labels].setStyleSheet("""
                                                        QLabel {border: 1px solid #ffaa00;}
                                                        QLabel:hover {border: 2px solid #ffaa00;}
                                                        """)

        self.clipboard_labels[labels].setFrameShape(QtWidgets.QFrame.Box)

        if tmp.endswith(".txt"):
            f = open(self.clipboards_location + tmp, 'r')
            data_type = f.readline().strip()
            # If contents is a list of files format appropriately
            if data_type == "FILE":
                files = literal_eval(f.read())
                text = "Files:\n"
                for filename in files:
                    text += os.path.basename(filename) + "\n"
                self.clipboard_labels[labels].setText(text)
            # Otherwise show plain text
            else:
                self.clipboard_labels[labels].setText(f.read())
            f.close()
            self.clipboard_labels[labels].setMargin(3)
        elif tmp.endswith(".bmp"):
            pixmap = QtGui.QPixmap(self.clipboards_location + tmp).scaled(131, 131, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.clipboard_labels[labels].setPixmap(pixmap)

        self.clipboard_labels[labels].setAlignment(QtCore.Qt.AlignCenter)
        self.clipboard_labels[labels].setWordWrap(True)
        self.clipboard_labels[labels].setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.clipboard_labels[labels].setToolTip("Clipboard: " + tmp[:-4])
        self.clipboard_labels[labels].id = tmp
        self.clipboard_labels[labels].mousePressEvent = self.labelClickEvent

        self.clipboard_labels[labels].customContext = Label_Context_Menu(tmp, self.clipboard_labels[labels], self.clipboards_location, self)
        self.clipboard_labels[labels].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.clipboard_labels[labels].customContextMenuRequested.connect(self.clipboard_labels[labels].customContext.on_menu_call)

        return labels + 1

    def closeButton(self, event):
        if event.button() == 1:
            self.MW.close()

    def deleteButton(self, event):
        if event.button() == 1:
            reply = QtWidgets.QMessageBox.warning(self.MW,
                                                  'Warning',
                                                  "You are about to clear all clipboards.\nDo you want to proceed?",
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                clipboards = []
                for labels in self.clipboard_labels:
                    clear(self.clipboards_location, self.clipboard_labels[labels].id[:-4])
                self.refresh()

    def addButton(self, event):
        if event.button() == 1:
            new_clipboard_id = 1
            current_clipboards = os.listdir(self.clipboards_location)
            current_clipboards_wo_extn = [i[:-4] for i in current_clipboards]
            while True:
                if str(new_clipboard_id) not in current_clipboards_wo_extn:
                    f = open(self.clipboards_location + str(new_clipboard_id) + ".txt", 'w')
                    f.write("TEXT\n")
                    f.close()
                    break
                else:
                    new_clipboard_id += 1
            self.refresh()

    def refreshButton(self, event):
        if event.button() == 1:
            self.refresh()

    def refresh(self):
        self.clipboard_labels = {}
        self.__init__(self.MW, self.clipboards_location, initial=False)

    def labelClickEvent(self, event):
        if event.button() == 1:
            widgets = self.centralwidget.children()
            for widget in widgets:
                hasGeo = getattr(widget, "mapToGlobal", None)
                if not callable(hasGeo):
                    continue
                if widget.mapToGlobal(event.pos()) == event.globalPos():
                    break
            data = getData()
            saveClipboard(self.clipboards_location, data)
            loadClipboard(self.clipboards_location, widget.id[:-4])
            data["current_clipboard"] = widget.id[:-4]
            setData(data)
            if data["close_on_gui_select"]:
                self.MW.close()
            else:
                self.refresh()

class Label_Context_Menu():
    def __init__(self, id, label, clipboards_location, parent):
        self.id = id
        self.label = label
        self.clipboards_location = clipboards_location
        self.parent = parent
        self.menu = QtWidgets.QMenu(self.label)
        self.menu.addAction(QtWidgets.QAction('clear', self.label))
        self.menu.addAction(QtWidgets.QAction('view', self.label))
        self.menu.addSeparator()
        self.menu.addAction(QtWidgets.QAction('switch', self.label))

    def on_menu_call(self, point):
        action = self.menu.exec_(self.label.mapToGlobal(point))
        if action != None:
            if action.text() == "clear":
                clear(self.clipboards_location, self.id[:-4])
                self.parent.refresh()

            elif action.text() == "view":
                if self.id.endswith(".txt"):
                    self.label.Form = QtWidgets.QWidget()
                    self.label.ui = GUI.Text_Explorer()
                    self.label.ui.setupUi(self.label.Form, self.label.text(), self.parent.MW.styleSheet(), self.id[:-4])
                    self.label.Form.show()

                elif self.id.endswith(".bmp"):
                    view_single(self.clipboards_location, self.id[:-4])

            elif action.text() == "switch":
                data = getData()
                saveClipboard(self.clipboards_location, data)
                loadClipboard(self.clipboards_location, self.id[:-4])
                data["current_clipboard"] = self.id[:-4]
                setData(data)
                self.parent.refresh()
