from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import clipboard

GRID_SPACING = 6
CLIPBOARD_LABEL_SIZE = 130
BUTTONS_SPACING = 4


class ClipboardSelector(QtWidgets.QWidget):

    # TODO ClipboardSelector

    def __init__(self, db_mgr):
        super().__init__()
        self.db_manager = db_mgr

        # Setup window
        self.setWindowTitle('Multi-Clipboard')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QMenu { border: 1px solid #000; }
            QMenu::item { padding: 2px 20px 2px 20px; }
            QMenu::item:selected { color: #000000; }
            QWidget { color: #b1b1b1; background-color: #323232; }
            QWidget:item:selected { background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
            QLabel { border: 1px solid #b1b1b1; }
            QLabel:hover { border: 2px solid #ffaa00; }
        """)
        self.setWindowOpacity(db_mgr.opacity)

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
        self.grid_layout = QtWidgets.QGridLayout()
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

            self.grid_layout.addWidget(self.create_clipboard_label(_id), _row, _col)

        if clipboards_total < 6:
            self.grid_layout.addLayout(self.create_buttons(), 0, clipboards_total)
        else:
            self.grid_layout.addLayout(self.create_buttons(), 0, 5)

        # self.setStyleSheet("background-color: red")

        self.centre()
        self.show()

    def create_clipboard_label(self, clipboard_id):
        label = QtWidgets.QLabel()
        label.setFixedSize(CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE)
        label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        label.clipboard_id = clipboard_id

        # Get the clipboard and check if it is valid
        clipboard_contents = self.db_manager.get_clipboard(clipboard_id)
        if clipboard_contents is None:
            clipboard_contents = {'type' : -1, 'content' : '', 'preview' : 'No Preview'}

        # Decide on what is being shown in the clipboard
        if clipboard.CF_PREVIEW_RELATIONS[clipboard_contents['type']] != 0:
            label.setText(clipboard_contents['preview'])
            label.setMargin(3)
        elif clipboard_contents['type'] == clipboard.CF_IMAGES:
            image = QtGui.QPixmap()
            image.loadFromData(clipboard_contents['preview'], 'JPEG')
            image = image.scaled(CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(image)
        else:
            label.setText('Preview not avaiable')
            label.setMargin(3)

        # Formatting
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        if self.db_manager.html_as_plain_text:
            label.setTextFormat(QtCore.Qt.PlainText)
        label.setToolTip("Clipboard: " + str(clipboard_id))

        # If this is the currently selected clipboard, show the user
        if self.db_manager.current_clipboard == clipboard_id:
            label.setStyleSheet("""QLabel {border: 1px solid #ffaa00;} QLabel:hover {border: 2px solid #ffaa00;}""")

        return label

    def create_buttons(self):
        layout = QtWidgets.QGridLayout()
        layout.setGeometry(QtCore.QRect(0, 0, CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE))
        layout.setSpacing(BUTTONS_SPACING)
        layout.setContentsMargins(0, 0, 0, 0)

        # Size of each label with spacing considered
        label_size = (CLIPBOARD_LABEL_SIZE - BUTTONS_SPACING) / 2

        # Data to setup buttons to stop repeating lines [img, onclick, row, col]
        button_data = [
            ['images/add.png', self.add_button, 0, 0],
            ['images/settings.png', self.settings_button, 0, 1],
            ['images/delete.png', self.clear_button, 1, 0],
            ['images/close.png', self.close_button, 1, 1]
        ]

        for button in button_data:
            tmp_btn = QtWidgets.QLabel()
            tmp_btn.setGeometry(QtCore.QRect(0, 0, label_size, label_size))
            tmp_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            icon = QtGui.QPixmap(button[0])
            icon = icon.scaled(label_size, label_size, QtCore.Qt.KeepAspectRatio)
            tmp_btn.setPixmap(icon)
            tmp_btn.mousePressEvent = button[1]
            layout.addWidget(tmp_btn, button[2], button[3])

        return layout

    def centre(self):
        # Thanks to https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def add_button(self, event):
        print ('Add clipboard')

    def close_button(self, event):
        if event.button() == 1:
            self.close()

    def clear_button(self, event):
        print('Clear all clipboards')

    def settings_button(self, event):
        print('Open Settings')


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
