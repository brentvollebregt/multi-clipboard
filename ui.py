from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import clipboard

GRID_SPACING = 5
CLIPBOARD_LABEL_SIZE = 130


class ClipboardSelector(QtWidgets.QWidget):

    # TODO ClipboardSelector

    def __init__(self, db_mgr):
        super().__init__()
        self.db_manager = db_mgr

        # Setup window
        self.setWindowTitle('Multi-Clipboard')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        clipboard_ids = self.db_manager.get_clipboard_ids()

        # Calculating grid size
        clipboards_total = len(clipboard_ids)
        if clipboards_total < 6:
            rows = 1
            cols = clipboards_total + 1
        else:
            rows = int(clipboards_total / 6) + 1
            cols = 6
        self.setGeometry(
            10,
            10,
            ((CLIPBOARD_LABEL_SIZE + GRID_SPACING) * cols) + GRID_SPACING,
            ((CLIPBOARD_LABEL_SIZE + GRID_SPACING) * rows) + GRID_SPACING
        )

        # Setup grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.grid_layout.setSpacing(GRID_SPACING)
        self.grid_layout.setContentsMargins(GRID_SPACING, GRID_SPACING, GRID_SPACING, GRID_SPACING)

        for position, _id in enumerate(clipboard_ids):
            if position < 5:
                # Deals with the first 5 to make space for the buttons
                _col = position
                _row = 0
            else:
                _row = int((position + 1) / 6)
                _col = int((position + 1) % 6)

            self.grid_layout.addWidget(self.create_clipboard_label(position), _row, _col)

        if clipboards_total < 6:
            self.grid_layout.addWidget(self.create_clipboard_label('BUTTONS'), 0, clipboards_total)
        else:
            self.grid_layout.addWidget(self.create_clipboard_label('BUTTONS'), 0, 5)

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
        label.setText("TMP (" + str(clipboard_id) + ")")

        label.setGeometry(QtCore.QRect(0, 0, CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE))
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
