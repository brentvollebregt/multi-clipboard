import os
from pynput import keyboard
import socket
import threading
from db import DatabaseManager
import utils
import ui


# Startup file statics
STARTUP_FILE = os.getenv('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\multi-clipboard.vbs'
STARTUP_COMMAND = 'python ' + os.path.dirname(os.path.realpath(__file__)) + '\\multi_clipboard.py'

# Key listener statics
LISTENER_COMBINATION = [
    keyboard.Key.ctrl_l,
    keyboard.Key.cmd,
    keyboard.KeyCode(char='c')
]

# Server statics
SERVER_ARE_YOU_RUNNING = b'Running?'
SERVER_YES = b'Yes'
SERVER_STOP = b'Stop'
SERVER_LOCK_FILE = os.path.dirname(os.path.realpath(__file__)) + '\.server_lock'


def start_listener():
    """ Start an instance of ListenerThread so the main thread can continue """
    listener_thread = ListenerThread()
    listener_thread.start()


def stop_listener():
    """ Tell the current running server to stop, must check is_listener_running() before calling """
    f = open(SERVER_LOCK_FILE, 'r')
    port = int(f.readline())
    f.close()
    server = ('127.0.0.1', port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(SERVER_STOP, server)


def is_listener_running():
    """ Check if the listener is running, returns a bool"""
    if os.path.isfile(SERVER_LOCK_FILE):
        # If file exists, get the port
        f = open(SERVER_LOCK_FILE, 'r')
        port = int(f.readline())
        f.close()
        server = ('127.0.0.1', port)

        # Send packet and then wait for reply
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1.0)
        client_socket.sendto(SERVER_ARE_YOU_RUNNING, server)
        try:
            message, server = client_socket.recvfrom(1024)
            if message == SERVER_YES:
                return True
        except socket.timeout:
            pass
        except ConnectionResetError:
            pass

    return False


def setup_listener_auto_start():
    """ Creates startup file with the correct command """
    f = open(STARTUP_FILE, 'w')
    f.write('Set oShell = WScript.CreateObject ("WScript.Shell")\n')
    f.write('oShell.run "' + STARTUP_COMMAND + '", 0, True')
    f.close()


def remove_listener_auto_start():
    """ Removes the startup file """
    os.remove(STARTUP_FILE)


def is_listener_auto_start():
    """ Checks to see if the startup file exists """
    return os.path.isfile(STARTUP_FILE)


class ListenerThread(threading.Thread):
    """ A listener thread for a key combination and a server to close the listener on command """

    keys_pressed = set()

    def __init__(self):
        super(ListenerThread, self).__init__()

    def run(self):
        """ When .start() is called, start the server in another thread then run the listener in this thread """
        server_thread = threading.Thread(target=self.server)
        server_thread.start()
        self.listen() # Just run this in the current thread

    def server(self):
        """ Create a local server. Wait for packets coming and and act accordingly """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('127.0.0.1', 0))

        f = open(SERVER_LOCK_FILE, 'w')
        f.write(str(server_socket.getsockname()[1]))
        f.close()

        while True:
            message, address = server_socket.recvfrom(1024)
            if message == SERVER_ARE_YOU_RUNNING:
                server_socket.sendto(SERVER_YES, address)
            elif message == SERVER_STOP:
                self.listener.stop()
                os.remove(SERVER_LOCK_FILE)
                break

    def listen(self):
        """ Start a listener and join it to this thread """
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()

    def on_press(self, key):
        """ When a key is pressed, check if it completes the combination of key presses """
        if key in LISTENER_COMBINATION:
            self.keys_pressed.add(key)
            if all([key in self.keys_pressed for key in LISTENER_COMBINATION]):
                # Make sure there isn't already a GUI_Thread running
                for thread in threading.enumerate():
                    if thread.getName() == 'GUI_Thread' and thread.is_alive():
                        break
                else:
                    # Thread the GUI so it doesn't block
                    ui_thread = threading.Thread(target=self.start_multi_clipboard)
                    ui_thread.setDaemon(False)
                    ui_thread.setName('GUI_Thread')
                    ui_thread.start()

    def on_release(self, key):
        """ When a key is released, remove it from the set remembering keys"""
        if key in LISTENER_COMBINATION and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def start_multi_clipboard(self):
        """ Start the main GUI when called with a new instance of db_manager """
        db_manager = DatabaseManager()
        utils.store_clipboard(db_manager)
        ui.show_clipboard_selector(db_manager)


if __name__ == "__main__":
    if not is_listener_running():
        start_listener()
