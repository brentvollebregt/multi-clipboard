from multi_clipboard import clipboard
from multi_clipboard import utils
from multi_clipboard import listener
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


# Location of the images folder
IMAGES_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\images'

# Static values for the GUI - for customisation
GRID_SPACING = 6
CLIPBOARD_LABEL_SIZE = 130
BUTTONS_SPACING = 4
BUTTON_IMAGE_SIZE_REDUCTION = 15
SETTINGS_DISTANCE_ABOVE_PARENT = 5


class ClipboardSelector(QtWidgets.QWidget):
    """ The main window for the clipboard selection GUI"""

    focus_enabled = False
    current_focus = None

    def __init__(self, db_mgr):
        super().__init__()
        self.db_manager = db_mgr

        # Setup window: title, flags, stylesheet, opacity
        self.setWindowTitle('Multi Clipboard')
        if self.db_manager.stay_on_top and self.db_manager.disable_frame:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        elif self.db_manager.stay_on_top:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        elif self.db_manager.disable_frame:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(
            'QMenu { border: 1px solid #000; }'
            'QMenu::item { padding: 2px 20px 2px 20px; }'
            'QMenu::item:selected { color: #000000; }'
            'QWidget { color: #b1b1b1; background-color: #323232; }'
            'QWidget:item:selected { background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a); }'
            'QLabel { border: 1px solid #b1b1b1; }'
            'QLabel:hover { border: 2px solid #ffaa00; }'
            'QLabel:focus { border: 2px solid #ffaa00; }'
        )
        self.setWindowOpacity(self.db_manager.opacity)

        clipboard_ids = self.db_manager.get_clipboard_ids()

        # Calculating grid and window size
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

        # Add clipboards
        for position, _id in enumerate(clipboard_ids):
            if position < 5:
                # If there are less than 5 clipboards (to account for settings button)
                _col = position
                _row = 0
            else:
                _row = int((position + 1) / 6)
                _col = int((position + 1) % 6)

            self.grid_layout.addWidget(self.create_clipboard_label(_id), _row, _col)

        # Add buttons
        if clipboards_total < 6:
            self.grid_layout.addLayout(self.create_buttons(), 0, clipboards_total)
        else:
            self.grid_layout.addLayout(self.create_buttons(), 0, 5)

        self.centre()
        self.show()

    def create_clipboard_label(self, clipboard_id):
        """ Create a label for a particular clipboard id """
        label = QtWidgets.QLabel()
        label.setFixedSize(CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE)
        label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        label.clipboard_id = clipboard_id

        # Get the clipboard and check if it is valid
        clipboard_contents = self.db_manager.get_clipboard(clipboard_id)
        if clipboard_contents is None:
            clipboard_contents = {'type' : -1, 'content' : '', 'preview' : 'No Preview'}

        # Decide on what is being shown in the clipboard (preview)
        if clipboard.CF_PREVIEW_RELATIONS[clipboard_contents['type']] != 0:
            label.setText(clipboard_contents['preview'])
            label.setMargin(3)
        elif clipboard_contents['type'] == clipboard.CF_IMAGES:
            image = QtGui.QPixmap()
            image.loadFromData(clipboard_contents['preview'], 'JPEG')
            image = image.scaled(CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(image)
        else:
            label.setText('Preview not available')
            label.setMargin(3)

        # Formatting
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        label.setToolTip("Clipboard: " + str(clipboard_id))

        # If this is the currently selected clipboard, show the user
        if self.db_manager.current_clipboard == clipboard_id:
            label.setStyleSheet(
                'QLabel {border: 1px solid #ffaa00;}'
                'QLabel:hover {border: 2px solid #ffaa00;}'
                'QLabel:focus {border: 2px solid #ffaa00;}'
            )

        # On click
        label_click = self.LabelClick(clipboard_id, self, label)
        label.mousePressEvent = label_click.on_click

        return label

    def create_buttons(self):
        """ Create the buttons for the right hand side of the GUI """
        # Create base label
        layout = QtWidgets.QGridLayout()
        layout.setGeometry(QtCore.QRect(0, 0, CLIPBOARD_LABEL_SIZE, CLIPBOARD_LABEL_SIZE))
        layout.setSpacing(BUTTONS_SPACING)
        layout.setContentsMargins(0, 0, 0, 0)

        # Size of each label with spacing considered
        label_size = (CLIPBOARD_LABEL_SIZE - BUTTONS_SPACING) / 2

        # Data to setup buttons to stop repeating lines [img, onclick, row, col, tooltip]
        button_data = [
            [IMAGES_FOLDER + '\\add.png', self.add_button, 0, 0, 'Add a new empty clipboard'],
            [IMAGES_FOLDER + '\\settings.png', self.settings_button, 0, 1, 'Open the settings'],
            [IMAGES_FOLDER + '\\delete.png', self.clear_button, 1, 0, 'Delete all clipboards'],
            [IMAGES_FOLDER + '\\close.png', self.close_button, 1, 1, 'Close this window']
        ]

        # Setup each button with data provided above
        for button in button_data:
            tmp_btn = QtWidgets.QLabel()
            tmp_btn.setFixedSize(label_size, label_size)
            tmp_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            icon = QtGui.QPixmap(button[0])
            icon = icon.scaled(label_size - BUTTON_IMAGE_SIZE_REDUCTION, label_size - BUTTON_IMAGE_SIZE_REDUCTION, QtCore.Qt.KeepAspectRatio)
            tmp_btn.setPixmap(icon)
            tmp_btn.setAlignment(QtCore.Qt.AlignCenter)
            tmp_btn.setToolTip(button[4])
            tmp_btn.mousePressEvent = button[1]
            layout.addWidget(tmp_btn, button[2], button[3])

        return layout

    def centre(self):
        """ Centre the window relative to the active display """
        # Thanks to https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def refresh(self):
        """ Refresh the whole GUI"""
        self.close()
        self.__init__(self.db_manager)

    def add_button(self, event):
        """ Event for the add button """
        utils.create_blank_clipboard(self.db_manager)
        self.refresh()

    def close_button(self, event):
        """ Event for the close button """
        if event.button() == 1:
            self.close()

    def clear_button(self, event):
        """ Event for the clear button """
        utils.delete_stored_clipboards(self.db_manager, self.db_manager.get_clipboard_ids())
        self.refresh()

    def settings_button(self, event):
        """ Event for the settings button """
        settings_window = self.SettingsWindow(self)
        settings_window.show()

    def keyPressEvent(self, event):
        """ Detecting keypress events globally to setup tab selection"""
        # If tab has been pressed and the tab selections havent been setup
        if event.key() == QtCore.Qt.Key_Tab and not self.focus_enabled:
            self.focus_enabled = True
            child_count = self.grid_layout.count()
            # Set all clipboards focus policies
            for child_index in range(child_count):
                if self.grid_layout.itemAt(child_index).widget() is not None:
                    self.grid_layout.itemAt(child_index).widget().setFocusPolicy(QtCore.Qt.StrongFocus)
            # Set the focus to the first clipboard
            self.grid_layout.itemAt(0).widget().setFocus()

        # If enter is pressed and we have setup tab selection
        elif event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return] and self.focus_enabled:
            # Send a left click event to the currently focused widget
            event = QtCore.QEvent(QtCore.QEvent.MouseButtonPress)
            event.button = lambda: 1
            self.focusWidget().mousePressEvent(event)

    class LabelClick:
        """ Handler for left and right clicks on a label """

        def __init__(self, clipboard_id, parent, label):
            self.clipboard_id = clipboard_id
            self.parent = parent
            self.label = label

        def on_click(self, event):
            """ When clicked, decide what to do """
            if event.button() == 1:
                # If this is a left click, set the clipboard and close if setting is true
                utils.set_clipboard(self.parent.db_manager, self.clipboard_id)
                if self.parent.db_manager.close_on_select:
                    self.parent.close()
                else:
                    self.parent.refresh()
            elif event.button() == 2:
                # If this is a right click, open context menu
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
        """ Settings window for the main clipboard GUI """

        SETTINGS_GRID_SPACING = 4
        SETTINGS_TILE_SIZE = 60

        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            # Setup settings window
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.setStyleSheet('QWidget {color: #b1b1b1; background-color: #323232; border: 0px;}')
            self.setWindowOpacity(1)

            # Setup grid layout
            self.grid_layout = QtWidgets.QGridLayout()
            self.setLayout(self.grid_layout)
            self.grid_layout.setSpacing(self.SETTINGS_GRID_SPACING)
            self.grid_layout.setContentsMargins(
                self.SETTINGS_GRID_SPACING,
                self.SETTINGS_GRID_SPACING,
                self.SETTINGS_GRID_SPACING,
                self.SETTINGS_GRID_SPACING
            )

            # Calculate window size based off **static** value of how many buttons/inputs we will have
            items = 7
            self.setFixedSize(
                (items * (self.SETTINGS_GRID_SPACING + self.SETTINGS_TILE_SIZE)) + self.SETTINGS_GRID_SPACING,
                self.SETTINGS_TILE_SIZE + (2 * self.SETTINGS_GRID_SPACING)
            )

            # Setup general toggle buttons
            self.close_on_select_button = self.create_basic_button(
                'Close on Select',
                self.close_on_select_button_click,
                'Close the widow when a clipboard is selected'
            )
            self.grid_layout.addWidget(self.close_on_select_button, 0, 0)

            self.stay_on_top_button = self.create_basic_button(
                'Stay on Top',
                self.stay_on_top_button_click,
                'Keep the window on top of all windows'
            )
            self.grid_layout.addWidget(self.stay_on_top_button, 0, 1)

            self.disable_frame_button = self.create_basic_button(
                'Disable Frame',
                self.disable_frame_button_click,
                'Disable the frame around the window\n(includes the minimise and close button)'
            )
            self.grid_layout.addWidget(self.disable_frame_button, 0, 2)

            # Setup opacity QSpinBox
            self.opacity_spin = QtWidgets.QSpinBox()
            self.opacity_spin.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            self.opacity_spin.setMaximum(100)
            self.opacity_spin.setMinimum(0)
            self.opacity_spin.setStyleSheet('QSpinBox {border: 1px solid #ffffff; font: 16pt; color: white;}')
            self.opacity_spin.setToolTip('Set the opacity of the main window')
            self.opacity_spin.valueChanged.connect(self.opacity_edit)
            self.grid_layout.addWidget(self.opacity_spin, 0, 3)

            # Setup listener toggle buttons
            self.toggle_listener_button = self.create_basic_button(
                'Toggle Listener',
                self.toggle_listener_button_click,
                'Turn the listener on/off\nPress Ctrl + Windows + C to open multi clipboard when on'
            )
            self.grid_layout.addWidget(self.toggle_listener_button, 0, 4)

            self.toggle_listener_auto_start_button = self.create_basic_button(
                'Listener Autostart',
                self.toggle_listener_auto_start_button_click,
                'Put a file in the startup folder to start the listener on startup'
            )
            self.grid_layout.addWidget(self.toggle_listener_auto_start_button, 0, 5)

            # Setup close button
            icon = QtGui.QPixmap(IMAGES_FOLDER + '\\close.png')
            icon = icon.scaled(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE, QtCore.Qt.KeepAspectRatio)
            self.close_label = QtWidgets.QLabel()
            self.close_label.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            self.close_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.close_label.setStyleSheet(
                'QLabel {border: 1px solid #ffffff; font: 8pt; color: white;}'
                'QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}'
            )
            self.close_label.setPixmap(icon)
            self.close_label.setAlignment(QtCore.Qt.AlignCenter)
            self.close_label.setToolTip('Close settings')
            self.close_label.mousePressEvent = self.close_button_click
            self.grid_layout.addWidget(self.close_label, 0, 6)

            self.position_above_parent()
            self.set_values()

        def create_basic_button(self, text, onclick, tooltip):
            """ Create a basic settings button with text and a onclick method """
            tmp_btn = QtWidgets.QLabel()
            tmp_btn.setFixedSize(self.SETTINGS_TILE_SIZE, self.SETTINGS_TILE_SIZE)
            tmp_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            tmp_btn.setText(text)
            tmp_btn.setWordWrap(True)
            tmp_btn.setMargin(3)
            tmp_btn.setAlignment(QtCore.Qt.AlignCenter)
            tmp_btn.mousePressEvent = onclick
            tmp_btn.setToolTip(tooltip)
            return tmp_btn

        def position_above_parent(self):
            """ Position the settings GUI above the parent (main clipboard GUI) """
            parents_geometry = self.parent.frameGeometry()
            parent_top = parents_geometry.y()
            parent_center = parents_geometry.x() + (parents_geometry.width() / 2)

            # Calculate positions of new window based off parent
            my_geometry = self.frameGeometry()
            my_x = parent_center - (my_geometry.width() / 2)
            my_y = parent_top - my_geometry.height() - SETTINGS_DISTANCE_ABOVE_PARENT
            self.move(my_x, my_y)

        def set_values(self):
            """ Update the display/value for each label depending on real states """
            self.opacity_spin.setValue(self.parent.db_manager.opacity * 100)

            settings_label_pairs = [
                [self.parent.db_manager.close_on_select, self.close_on_select_button],
                [self.parent.db_manager.stay_on_top, self.stay_on_top_button],
                [self.parent.db_manager.disable_frame, self.disable_frame_button],
                [listener.is_listener_running(), self.toggle_listener_button],
                [listener.is_listener_auto_start(), self.toggle_listener_auto_start_button],
            ]

            # Go through each index of settings_label_pairs checking value and then setting label style sheet
            for pair in settings_label_pairs:
                if pair[0]:
                    pair[1].setStyleSheet(
                        'QLabel {border: 1px solid #ffaa00; font: 8pt; color: #ffaa00;}'
                        'QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}'
                    )
                else:
                    pair[1].setStyleSheet(
                        'QLabel {border: 1px solid #ffffff; font: 8pt; color: white;}'
                        'QLabel:hover {border: 2px solid #ffaa00; color: #ffaa00;}'
                    )

        def close_on_select_button_click(self, e):
            """ Event handler for close_on_select_button """
            self.parent.db_manager.close_on_select = not self.parent.db_manager.close_on_select
            self.set_values()

        def stay_on_top_button_click(self, e):
            """ Event handler for stay_on_top_button """
            self.parent.db_manager.stay_on_top = not self.parent.db_manager.stay_on_top
            self.set_values()

        def disable_frame_button_click(self, e):
            """ Event handler for disable_frame_button """
            self.parent.db_manager.disable_frame = not self.parent.db_manager.disable_frame
            self.set_values()

        def opacity_edit(self, e):
            """ Event handler for the edit of opacity_edit """
            self.parent.db_manager.opacity = self.opacity_spin.value() / 100
            self.set_values()

        def toggle_listener_button_click(self, e):
            """ Event handler for toggle_listener_button """
            if listener.is_listener_running():
                listener.stop_listener()
            else:
                listener.start_listener()
            self.set_values()

        def toggle_listener_auto_start_button_click(self, e):
            """ Event handler for toggle_listener_auto_start_button """
            if listener.is_listener_auto_start():
                listener.remove_listener_auto_start()
            else:
                listener.setup_listener_auto_start()
            self.set_values()

        def close_button_click(self, e):
            """ Close the window when the close button is pressed """
            if e.button() == 1:
                self.close()


def show_clipboard_selector(db_manager):
    """ Open the main GUI application """
    app = QtWidgets.QApplication(sys.argv)
    cs = ClipboardSelector(db_manager)
    app.exec_()


def show_unsupported_clipboard_warning():
    """ Show a message warning the user about an unsupported clipboard """
    app = QtWidgets.QApplication([])
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(
        'The current item on your clipboard is not supported.\n'
        'The application is unable to detect the type of the clipboard so it must stop.\n\n'
        'No data has been lost. Changing the contents of the clipboard will fix this'
    )
    msg.setWindowTitle("Fatal Error")
    msg.show()
    msg.raise_()
    msg.activateWindow()
    app.exec_()
