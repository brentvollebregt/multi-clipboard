from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import clipboard


class ClipboardSelector(QtWidgets.QWidget):

    # TODO ClipboardSelector

    def __init__(self, db_mgr):
        super().__init__()
        self.db_manager = db_mgr

        # Calculating grid size
        clipboards_total = len(self.db_manager.get_clipboard_ids())
        if clipboards_total < 6:
            rows = 1
            cols = clipboards_total + 1
        else:
            rows = 100 # TODO Calculate rows needed
            cols = 6

        # Set window title and size
        self.setWindowTitle('Multi-Clipboard')
        self.setGeometry(10, 10, 850, 150)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # Setup grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)

        self.grid_layout.addWidget(self.create_clipboard_label('1'), 0, 0)
        self.grid_layout.addWidget(self.create_clipboard_label('2'), 0, 1)
        self.grid_layout.addWidget(self.create_clipboard_label('3'), 0, 2)
        self.grid_layout.addWidget(self.create_clipboard_label('4'), 0, 3)
        self.grid_layout.addWidget(self.create_clipboard_label('5'), 0, 4)
        self.grid_layout.addWidget(self.create_clipboard_label('6'), 0, 5)

        self.setStyleSheet("background-color: red")

        self.centre()
        self.show()

    def create_clipboard_label(self, clipboard_id):
        label = QtWidgets.QLabel()
        label.clipboard_id = clipboard_id
        # clipboard_contents = self.db_manager.get_clipboard(clipboard_id)
        #
        # if clipboard_contents['type'] == clipboard.CF_PLAIN_TEXT:
        #     label.setText("CF_PLAIN_TEXT")
        # elif clipboard_contents['type'] == clipboard.CF_RTF:
        #     label.setText("CF_RTF")
        # elif clipboard_contents['type'] == clipboard.CF_UNICODE_TEXT:
        #     label.setText("CF_UNICODE_TEXT")
        # elif clipboard_contents['type'] == clipboard.CF_HTML:
        #     label.setText("CF_HTML")
        # elif clipboard_contents['type'] == clipboard.CF_FILES:
        #     label.setText("CF_FILES")
        # elif clipboard_contents['type'] == clipboard.CF_IMAGES:
        #     label.setText("CF_IMAGES")
        # else:
        #     label.setText("Corrupted (" + str(clipboard_id) + ')')
        label.setText("TMP")

        label.setGeometry(QtCore.QRect(0, 0, 130, 130))
        label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("background-color: blue")
        return label

    def centre(self):
        # Thanks to https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def get_clipboards(self):
        pass

    def add_button(self):
        pass

    def close_button(self):
        pass

    def clear_button(self):
        pass

    def settings_button(self):
        pass


class SettingsWindow:
    # TODO SettingsWindow
    def __init__(self):
        pass


class UnsupportedClipboardWarning:
    # TODO UnsupportedClipboardWarning
    def __init__(self):
        pass


def show_clipboard_selector(db_manager):
    print("UI placeholder")
    app = QtWidgets.QApplication(sys.argv)
    ex = ClipboardSelector(db_manager)
    sys.exit(app.exec_())


def show_unsupported_clipboard_warning():
    print("UnsupportedClipboardWarning placeholder")
