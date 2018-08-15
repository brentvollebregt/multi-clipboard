# Mutli Clipboard
Switch clipboard contents using a simple GUI<br />
Images, text, files and other formats are supported with unlimited amounts of saved clipboards able to be created.<br />
The idea of this is to easily switch clipboards with a simple click in a GUI.

## GUI

![GUI Example](http://i.imgur.com/dp42h1m.jpg "GUI Example")

## What Is This?
This is my solution to constantly overwriting my clipboard. It is a GUI that acts like a hotbar, click on a virtual clipboard to place it on your actual clipboard. Some command line support has also been added in the form of setting and clearing clipboards.

## Getting Started

### Prerequisites
 - Python (tested on 3.4+)
 - Windows

### Installation and Usage
You can install this project using this repository by following these steps:
1. Clone/download this repo
2. Open cmd/terminal and cd to the project
3. Execute ```pip install -r requirements.txt``` and [install this if pywin32 doesn't install](https://sourceforge.net/projects/pywin32/files/pywin32/)

To run the GUI, simply run the ```multi_clipboard.py``` script with no parameters. Alternatively use ```run.vbs``` to open the GUI with no console (can be used for key shortcuts).

### GUI Usage
* Click on clipboard to switch to it (will close automatically on selection by default)
* Right click menu on each clipboard to individually delete/set
* Click on the trash to delete all clipboards
* Click on the plus button to create a new clipboard
* Settings for the GUI can be toggled easily in settings window

### Command Line Usage
* `clipboards.py` - Opens GUI
* `clipboards.py -s [clipboard]` - Will load data from that clipboard if it exists
* `clipboards.py -c *` - Delete all clipboards
* `clipboards.py -c 1` - Delete clipboard 1

#### So What Happens If...
 - I delete all clipboards? -> Clipboard 0 will be created with the current contents
 - I delete the clipboard I am currently on? -> Nothing, your clipboard will be saved back to that clipboard later.
 - I am shown an error saying my clipboard isn't supported? -> Open up an issue with details on what your clipboard contents are, we can see if it can be supported

## Thanks to
* [Michael Robertson](https://github.com/MBRobertson) for adding file support in previous versions.

## Things that still are being done
 - Comment and label methods
 - Messages back in argument passing (print)
 - Put tool tips on buttons
 - Add new image to README
 - Add listener running on a server to wait for [Ctrl + Windows + C]
     - Add notes to readme for starting and stopping (--start-listener)
     - Optional import for pynput
        - Notify the user if not installed
     - Add autostart option
        - Put in settings to toggle
        - "Listen on Startup"
        - Put a vbs script in startup folder
        - Remove if toggled off
 - Convert to package format
    - Add setup.py
    - License
    - PyPI?
