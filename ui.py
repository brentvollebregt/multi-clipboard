from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import clipboard
import utils

GRID_SPACING = 6
CLIPBOARD_LABEL_SIZE = 130
BUTTONS_SPACING = 4


class ClipboardSelector(QtWidgets.QWidget):

    def __init__(self, db_mgr):
        super().__init__()
        self.db_manager = db_mgr

        # Setup window
        self.setWindowTitle('Multi-Clipboard')
        if self.db_manager.stay_on_top and self.db_manager.disable_frame:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        elif self.db_manager.stay_on_top:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        elif self.db_manager.disable_frame:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            QMenu { border: 1px solid #000; }
            QMenu::item { padding: 2px 20px 2px 20px; }
            QMenu::item:selected { color: #000000; }
            QWidget { color: #b1b1b1; background-color: #323232; }
            QWidget:item:selected { background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }
            QLabel { border: 1px solid #b1b1b1; }
            QLabel:hover { border: 2px solid #ffaa00; }
        """)
        self.setWindowOpacity(self.db_manager.opacity)

        clipboard_ids = self.db_manager.get_clipboard_ids()

        # Calculating grid size
        clipboards_total = len(clipboard_ids)
        if clipboards_total < 6:
            rows = 1
            cols = clipboards_total + 1
        else:
            rows = int(clipboards_total / 6) + 1
            cols = 6
        self.setFixedSize(
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
        # if self.db_manager.html_as_plain_text:
        #     label.setTextFormat(QtCore.Qt.PlainText) TODO If we have issues
        label.setToolTip("Clipboard: " + str(clipboard_id))

        # If this is the currently selected clipboard, show the user
        if self.db_manager.current_clipboard == clipboard_id:
            label.setStyleSheet("""QLabel {border: 1px solid #ffaa00;} QLabel:hover {border: 2px solid #ffaa00;}""")

        # On click
        label_click = self.LabelClick(clipboard_id, self, label)
        label.mousePressEvent = label_click.on_click

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

    def refresh(self):
        self.close()
        self.__init__(self.db_manager)

    def add_button(self, event):
        utils.create_blank_clipboard(self.db_manager)
        self.refresh()

    def close_button(self, event):
        if event.button() == 1:
            self.close()

    def clear_button(self, event):
        utils.delete_stored_clipboards(self.db_manager, self.db_manager.get_clipboard_ids())
        self.refresh()

    def settings_button(self, event):
        settings_window = self.SettingsWindow(self)
        settings_window.show()

    class LabelClick:

        def __init__(self, clipboard_id, parent, label):
            self.clipboard_id = clipboard_id
            self.parent = parent
            self.label = label

        def on_click(self, event):
            if event.button() == 1: # Check it is a right click
                utils.set_clipboard(self.parent.db_manager, self.clipboard_id)
                if self.parent.db_manager.close_on_select:
                    self.parent.close()
                else:
                    self.parent.refresh()
            elif event.button() == 2:
                menu = QtWidgets.QMenu(self.label)
                remove_action = QtWidgets.QAction('remove', self.label)
                menu.addAction(remove_action)
                menu.addSeparator()
                switch_action = QtWidgets.QAction('switch', self.label)
                menu.addAction(switch_action)
                action = menu.exec_(self.label.mapToGlobal(event.pos()))
                if action is not None:
                    if action == remove_action:
                        utils.delete_stored_clipboards(self.parent.db_manager, [self.clipboard_id])
                        self.parent.refresh()
                    elif action == switch_action:
                        utils.set_clipboard(self.parent.db_manager, self.clipboard_id)
                        self.parent.refresh()

    class SettingsWindow(QtWidgets.QWidget):

        SETTINGS_GRID_SPACING = 4
        SETTINGS_TILE_SIZE = 60

        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.setStyleSheet("QWidget {color: #b1b1b1; background-color: #323232; border: 0px;}")
            self.setWindowOpacity(1)

            self.grid_layout = QtWidgets.QGridLayout()
            self.setLayout(self.grid_layout)
            self.grid_layout.setSpacing(self.SETTINGS_GRID_SPACING)
            self.grid_layout.setContentsMargins(self.SETTINGS_GRID_SPACING, self.SETTINGS_GRID_SPACING, self.SETTINGS_GRID_SPACING, self.SETTINGS_GRID_SPACING)

            items = 5 # Manually set how many buttons/inputs we will have
            self.setFixedSize(
                (items * (self.SETTINGS_GRID_SPACING + self.SETTINGS_TILE_SIZE)) + self.SETTINGS_GRID_SPACING,
                self.SETTINGS_TILE_SIZE + (2 * self.SETTINGS_GRID_SPACING)
            )

            self.close_on_select_button = self.create_basic_button('Close on Select', self.close_on_select_button_click)
            self.grid_layout.addWidget(self.close_on_select_button, 0, 0)

            self.stay_on_top_button = self.create_basic_button('Stay on Top', self.stay_on_top_button_click)
            self.grid_layout.addWidget(self.stay_on_top_button, 0, 1)

            self.disable_frame_button = self.create_basic_button('Disable Frame', self.disable_frame_button_click)
            self.grid_layout.addWidget(self.disable_frame_button, 0, 2)

            self.opacity_spin = QtWidgets.QSpinBox()
            self.opacity_spin.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            self.opacity_spin.setMaximum(100)
            self.opacity_spin.setMinimum(0)
            self.opacity_spin.setStyleSheet("QSpinBox {border: 1px solid #ffffff; font: 16pt; color: white;}")
            self.opacity_spin.valueChanged.connect(self.opacity_edit)
            self.grid_layout.addWidget(self.opacity_spin, 0, 3)

            icon = QtGui.QPixmap('images/close.png')
            icon = icon.scaled(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE, QtCore.Qt.KeepAspectRatio)
            self.close_label = QtWidgets.QLabel()
            self.close_label.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            self.close_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.close_label.setStyleSheet("QLabel {border: 1px solid #ffffff; font: 8pt; color: white;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")
            self.close_label.setPixmap(icon)
            self.close_label.setAlignment(QtCore.Qt.AlignCenter)
            self.close_label.mousePressEvent = self.close_button_click
            self.grid_layout.addWidget(self.close_label, 0, 4)

            self.set_values()

        def create_basic_button(self, text, onclick):
            tmp_btn = QtWidgets.QLabel()
            tmp_btn.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            tmp_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            tmp_btn.setText(text)
            tmp_btn.setWordWrap(True)
            tmp_btn.setMargin(3)
            tmp_btn.setAlignment(QtCore.Qt.AlignCenter)
            tmp_btn.mousePressEvent = onclick
            return tmp_btn

        def set_values(self):
            self.opacity_spin.setValue(self.parent.db_manager.opacity * 100)

            if self.parent.db_manager.close_on_select:
                self.close_on_select_button.setStyleSheet("QLabel {border: 1px solid #ffaa00; font: 8pt; color: #ffaa00;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")
            else:
                self.close_on_select_button.setStyleSheet("QLabel {border: 1px solid #ffffff; font: 8pt; color: white;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")

            if self.parent.db_manager.stay_on_top:
                self.stay_on_top_button.setStyleSheet("QLabel {border: 1px solid #ffaa00; font: 8pt; color: #ffaa00;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")
            else:
                self.stay_on_top_button.setStyleSheet("QLabel {border: 1px solid #ffffff; font: 8pt; color: white;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")

            if self.parent.db_manager.disable_frame:
                self.disable_frame_button.setStyleSheet("QLabel {border: 1px solid #ffaa00; font: 8pt; color: #ffaa00;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")
            else:
                self.disable_frame_button.setStyleSheet("QLabel {border: 1px solid #ffffff; font: 8pt; color: white;} QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}")

        def close_on_select_button_click(self, e):
            self.parent.db_manager.close_on_select = not self.parent.db_manager.close_on_select
            self.set_values()

        def stay_on_top_button_click(self, e):
            self.parent.db_manager.stay_on_top = not self.parent.db_manager.stay_on_top
            self.set_values()

        def disable_frame_button_click(self, e):
            self.parent.db_manager.disable_frame = not self.parent.db_manager.disable_frame
            self.set_values()

        def opacity_edit(self, e):
            self.parent.db_manager.opacity = self.opacity_spin.value() / 100
            self.set_values()

        def close_button_click(self, e):
            if e.button() == 1:
                self.close()


class UnsupportedClipboardWarning:
    # TODO UnsupportedClipboardWarning
    def __init__(self):
        pass


def show_clipboard_selector(db_manager):
    app = QtWidgets.QApplication(sys.argv)
    cs = ClipboardSelector(db_manager)
    sys.exit(app.exec_())


def show_unsupported_clipboard_warning():
    print("UnsupportedClipboardWarning placeholder")
