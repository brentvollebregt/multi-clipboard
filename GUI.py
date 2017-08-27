from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setStyleSheet("""
        QMenu {
            border: 1px solid #000;
        }
        QMenu::item {
            padding: 2px 20px 2px 20px;
        }
        QMenu::item:selected {
            color: #000000;
        }
        QWidget {
            color: #b1b1b1;
            background-color: #323232;
        }
        QWidget:item:selected {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
        }
        QLabel:hover {
            border: 2px solid #ffaa00;
        }
        """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_6 = self.setup_static_button(710,10)
        self.label_7 = self.setup_static_button(780,10)
        self.label_8 = self.setup_static_button(710,80)
        self.label_9 = self.setup_static_button(780,80)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def setup_static_button(self, x, y): # Just removes repetition
        label = QtWidgets.QLabel(self.centralwidget)
        label.setGeometry(QtCore.QRect(x, y, 61, 61))
        label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        label.setFrameShape(QtWidgets.QFrame.Box)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

class Text_Explorer(QtWidgets.QDialog):
    def setupUi(self, Form, data, stylesheet, clipboard):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setStyleSheet(stylesheet)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setHtml(data)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        Form.setWindowTitle("Clipboard " + clipboard)
        QtCore.QMetaObject.connectSlotsByName(Form)
