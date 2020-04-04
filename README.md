# Multi Clipboard
Switch clipboard contents using a simple GUI<br />
Images, text, files and other formats are supported with unlimited amounts of saved clipboards able to be created.<br />
The idea of this is to easily switch clipboards with a simple click in a GUI. It comes with a built in listener for Ctrl + Windows + C

![Main GUI](https://nitratine.net/posts/multi-clipboard/main-gui.png)

## What Is This?
This is my solution to constantly overwriting my clipboard. It is a GUI that acts like a hotbar, click on a virtual clipboard to place it on your actual clipboard. Some command line support has also been added in the form of setting and clearing clipboards.

## Getting Started

### Prerequisites
 - Python >= 3.5
 - Windows

### Installation and Usage

#### Installing Via [PyPi](https://pypi.org/project/multi-clipboard/)
To install the package from PyPI, execute:

```
python -m pip install multi-clipboard
```

Now you can run the project anywhere using:

```
multi-clipboard
```

#### Installing Via the [Repository](https://github.com/brentvollebregt/multi-clipboard)
You can install this project using this repository by following these steps:
1. Clone/download the [repository](https://github.com/brentvollebregt/multi-clipboard)
2. Open cmd/terminal and cd into multi-clipboard using ```cd multi-clipboard```
3. Execute ```python setup.py install```

Now you can run the project anywhere using:

```
multi-clipboard
```

#### Running the Package From [Source](https://github.com/brentvollebregt/auto-py-to-exe/archive/master.zip)
Don't want to have to install the package? Follow these steps:
1. Clone/download the [repository](https://github.com/brentvollebregt/multi-clipboard)
2. Open cmd/terminal and cd into multi-clipboard using ```cd multi-clipboard```
3. Install requirements using ```python -m pip install -r requirements.txt``` and [install this if pywin32 doesn't install](https://github.com/mhammond/pywin32/releases)
4. Run the project using ```python -m multi_clipboard```

### GUI Usage
* Click on clipboard to switch to it (will close automatically on selection by default)
    - You can also use TAB to highlight the clipboards and then press ENTER to set the currently selected keyboard
* Right click menu on each clipboard to individually delete/set
* Click on the trash to delete all clipboards
* Click on the plus button to create a new clipboard
* Settings for the GUI can be toggled easily in settings window. In here you can:
    - Change window settings (opacity, frame, stay on top...)
    - Toggle the listener
    - Make the listener start on user login
    
### Opening the GUI With A Mouse Click
If you rather a double click opposed to typing `mutli-clipboard` in the terminal, open the project and then click the settings button. On the right you will see a button labeled "Create Shortcut"; clicking this will ask you where you want to save a shortcut script (VB script).

### Command Line Usage
* `multi-clipboard` - Opens GUI
* `multi-clipboard -s [clipboard]` - Will load data from that clipboard if it exists
* `multi-clipboard -c *` - Delete all clipboards
* `multi-clipboard -c 1` - Delete clipboard 1
* `multi-clipboard --start-listener` - Starts the listener if it isn't running
* `multi-clipboard --stop-listener` - Stops the listener if it's running
* `multi-clipboard --current` - Check what clipboard you are currently on

## The Listener
This package has a built in listener which listens for Ctrl + Windows + C (Left control). This can be enabled in the GUI's settings under "Toggle Listener" or by arguments as described above. This also comes with a feature to make the listener start on startup. To enable this, go into the GUI's settings and click "Listener Autostart" to toggle it on/off.

## GUI With Settings Open

![Main GUI with Settings](https://nitratine.net/posts/multi-clipboard/main-gui-with-settings-shown.png)

## Thanks to
* [Michael Robertson](https://github.com/MBRobertson) for adding file support in previous versions.

## Improvements That Can Be Made
- [ ] Save all the current sub-clipboards in a table for each virtual clipboard
    - One table references the clipboards table which also has preview in it
    - n many tables for each clipboard containing [type, content]. Will need to be re-constructed to correct formats when assigning e.g. bytes, string, tuple.
- [ ] Generate an executable
