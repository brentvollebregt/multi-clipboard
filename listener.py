import os
from pynput import keyboard
import socket
import threading


STARTUP_FOLDER = os.getenv('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
STARTUP_COMMAND = 'python ' + os.path.abspath(__file__)
LISTENER_COMBINATION = [
    keyboard.Key.ctrl_l,
    keyboard.Key.cmd,
    keyboard.KeyCode(char='c')
]


def start_listener():
    """ Start an instance of ListenerThread so the main thread can continue """
    listener_thread = ListenerThread()
    listener_thread.start()


def stop_listener():
    # Try and read the lock file with the port in it. Tell the port to stop if it exists
    pass


def is_listener_running():
    # Return a bool of whether the listener is currently running
    return False # TODO Return true if server is running


def setup_listener_auto_start():
    pass


def remove_listener_auto_start():
    pass


def is_listener_auto_start():
    return False # TODO Return true if file is found for autostart


class ListenerThread(threading.Thread):

    keys_pressed = set()

    def __init__(self):
        super(ListenerThread, self).__init__()

    def run(self):
        self.server_thread = threading.Thread(target=self.server)
        self.server_thread.start()
        self.listen() # Just run this in the current thread

    def server(self):
        while True:
            pass

    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if key in LISTENER_COMBINATION:
            self.keys_pressed.add(key)
            if all([key in self.keys_pressed for key in LISTENER_COMBINATION]):
                self.start_multi_clipboard()

    def on_release(self, key):
        if key in LISTENER_COMBINATION and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def start_multi_clipboard(self):
        print ("START")


if __name__ == "__main__":
    if not is_listener_running():
        start_listener()
