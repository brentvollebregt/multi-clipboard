import pynput
import socket
import threading


def start_listener():
    # Call a thread every time so it will keep running no matter where it came from
    pass


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


class Listener:

    keys_pressed = set()

    def __init__(self):
        # Create a thread for the listener and then start the server
        # Hold onto the listener object so we can stop it anytime (server kills listener then ends itself)
        pass

    def server(self):
        pass

    def listen(self):
        pass

    def on_key_press(self):
        pass

    def on_key_release(self):
        pass


if __name__ == "__main__":
    start_listener()
