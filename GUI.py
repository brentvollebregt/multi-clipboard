# Images from https://material.io/

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(851, 151)
        MainWindow.setWindowOpacity(0.9)
        MainWindow.setStyleSheet("QToolTip {\n"
"    border: 1px solid black;\n"
"    background-color: #ffa02f;\n"
"    padding: 1px;\n"
"    border-radius: 3px;\n"
"    opacity: 100;\n"
"}\n"
"QWidget {\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"}\n"
"QWidget:item:hover {\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"QWidget:item:selected {\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"QMenuBar::item {\n"
"    background: transparent;\n"
"}\n"
"QMenuBar::item:selected {\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"QMenuBar::item:pressed {\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 1 #212121, stop: 0.4 #343434\n"
"    /*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    \n"
"    );\n"
"    margin-bottom: -1px;\n"
"    padding-bottom: 1px;\n"
"}\n"
"QMenu {\n"
"    border: 1px solid #000;\n"
"}\n"
"QMenu::item {\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"QMenu::item:selected {\n"
"    color: #000000;\n"
"}\n"
"QWidget:disabled {\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"QAbstractItemView {\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"QWidget:focus {\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
"}\n"
"QLineEdit {\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"QPushButton {\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"QComboBox {\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"QComboBox:hover,\n"
"QPushButton:hover {\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"QComboBox:on {\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 0px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    /* just a single line */\n"
"    \n"
"    border-top-right-radius: 3px;\n"
"    /* same radius as the QComboBox */\n"
"    \n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(:/down_arrow.png);\n"
"}\n"
"QGroupBox:focus {\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"QTextEdit:focus {\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: 1px solid #222222;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"    height: 7px;\n"
"    margin: 0px 16px 0 16px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"    min-height: 20px;\n"
"    border-radius: 2px;\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: 1px solid #1b1b19;\n"
"    border-radius: 2px;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"    width: 14px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: 1px solid #1b1b19;\n"
"    border-radius: 2px;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"    width: 14px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::right-arrow:horizontal,\n"
"QScrollBar::left-arrow:horizontal {\n"
"    border: 1px solid black;\n"
"    width: 1px;\n"
"    height: 1px;\n"
"    background: white;\n"
"}\n"
"QScrollBar::add-page:horizontal,\n"
"QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"}\n"
"QScrollBar:vertical {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"    width: 7px;\n"
"    margin: 16px 0 16px 0;\n"
"    border: 1px solid #222222;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"    min-height: 20px;\n"
"    border-radius: 2px;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"    border: 1px solid #1b1b19;\n"
"    border-radius: 2px;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"    height: 14px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"    border: 1px solid #1b1b19;\n"
"    border-radius: 2px;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"    height: 14px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:vertical,\n"
"QScrollBar::down-arrow:vertical {\n"
"    border: 1px solid black;\n"
"    width: 1px;\n"
"    height: 1px;\n"
"    background: white;\n"
"}\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"QTextEdit {\n"
"    background-color: #242424;\n"
"}\n"
"QPlainTextEdit {\n"
"    background-color: #242424;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop: 1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"QCheckBox:disabled {\n"
"    color: #414141;\n"
"}\n"
"QDockWidget::title {\n"
"    text-align: center;\n"
"    spacing: 3px;\n"
"    /* spacing between items in the tool bar */\n"
"    \n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #323232, stop: 0.5 #242424, stop: 1 #323232);\n"
"}\n"
"QDockWidget::close-button,\n"
"QDockWidget::float-button {\n"
"    text-align: center;\n"
"    spacing: 1px;\n"
"    /* spacing between items in the tool bar */\n"
"    \n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #323232, stop: 0.5 #242424, stop: 1 #323232);\n"
"}\n"
"QDockWidget::close-button:hover,\n"
"QDockWidget::float-button:hover {\n"
"    background: #242424;\n"
"}\n"
"QDockWidget::close-button:pressed,\n"
"QDockWidget::float-button:pressed {\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"QMainWindow::separator {\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop: 1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px;\n"
"    /* spacing between items in the tool bar */\n"
"}\n"
"QMainWindow::separator:hover {\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 0.5 #b56c17 stop: 1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px;\n"
"    /* spacing between items in the tool bar */\n"
"}\n"
"QToolBar::handle {\n"
"    spacing: 3px;\n"
"    /* spacing between items in the tool bar */\n"
"    \n"
"    background: url(:/images/handle.png);\n"
"}\n"
"QMenu::separator {\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop: 1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"QTabBar::tab:last {\n"
"    margin-right: 0;\n"
"    /* the last selected tab has nothing to overlap with on the right */\n"
"    \n"
"    border-top-right-radius: 3px;\n"
"}\n"
"QTabBar::tab:first:!selected {\n"
"    margin-left: 0px;\n"
"    /* the last selected tab has nothing to overlap with on the right */\n"
"    \n"
"    border-top-left-radius: 3px;\n"
"}\n"
"QTabBar::tab:!selected {\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 1 #212121, stop: .4 #343434);\n"
"}\n"
"QTabBar::tab:selected {\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"QTabBar::tab:!selected:hover {\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    \n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 1 #212121, stop: 0.4 #343434, stop: 0.2 #343434, stop: 0.1 #ffaa00);\n"
"}\n"
"QRadioButton::indicator:checked,\n"
"QRadioButton::indicator:unchecked {\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background-color: qradialgradient( cx: 0.5, cy: 0.5, fx: 0.5, fy: 0.5, radius: 1.0, stop: 0.25 #ffaa00, stop: 0.3 #323232);\n"
"}\n"
"QCheckBox::indicator {\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"QRadioButton::indicator {\n"
"    border-radius: 6px;\n"
"}\n"
"QRadioButton::indicator:hover,\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/images/checkbox.png);\n"
"}\n"
"QCheckBox::indicator:disabled,\n"
"QRadioButton::indicator:disabled {\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"\n"
"QLabel:hover {\n"
"    border: 2px solid #ffaa00;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 131))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(False)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 10, 131, 131))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 10, 131, 131))
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(False)
        self.label_3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(290, 10, 131, 131))
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setText("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setOpenExternalLinks(False)
        self.label_4.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(570, 10, 131, 131))
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setOpenExternalLinks(False)
        self.label_5.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(710, 10, 61, 61))
        self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setOpenExternalLinks(False)
        self.label_6.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(780, 10, 61, 61))
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setText("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setWordWrap(True)
        self.label_7.setOpenExternalLinks(False)
        self.label_7.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(780, 80, 61, 61))
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_8.setFrameShape(QtWidgets.QFrame.Box)
        self.label_8.setText("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setOpenExternalLinks(False)
        self.label_8.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(710, 80, 61, 61))
        self.label_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_9.setFrameShape(QtWidgets.QFrame.Box)
        self.label_9.setText("")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setOpenExternalLinks(False)
        self.label_9.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

