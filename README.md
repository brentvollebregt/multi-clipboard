# Mutli Clipboard
Switch clipboard contents using easily using a command<br />
Images, text and files are supported and unlimited amounts of saved clipboards can be created.<br />
The idea of this is to easily switch keyboards with simple commands. Map commands to keys to use this easily.

## What This Does
This acts as a hotbar in a game would. The main feature of this project is the GUI but there is support for command line manipulation. It is made for situations where you find you are copying the same thing over and over again because you need to *temporarily* copy something.

## Installation/Setup
1. Install PIL if you are using Python 3 ( `pip install Pillow` )
2. Install PYQT5 ( `pip install pyqt5` )
3. Install pywin32 ( `pip install pypiwin32` or [Installer](https://sourceforge.net/projects/pywin32/files/pywin32/))

## GUI

![GUI Example](http://i.imgur.com/dp42h1m.jpg "GUI Example")

### Features
* Very easily switch clipboard contents
* Dark stylesheet and transparency
* Dynamically displays contents of clipboards
* Can view all clipboard contents easily
* Easily add and remove clipboards

### GUI Usage
*Use `clipboards.py view` to open the GUI*
* Click on clipboard to switch to it (auto close feature mentioned below)
* Right click menu on each clipboard
* Clear all clipboards option
* Easy refresh
* Can add from the GUI (will pick the lowest integer)
* Displays both text and images

### Command Line Usage
* `clipboards.py view` - Opens GUI (as stated above)
* `clipboards.py view 1` - Views clipboard 1
* `clipboards.py switch [clipboard]` - Will switch current clipboard to the clipboard specified
* `clipboards.py clear` - Clear all clipboards
* `clipboards.py clear 1` - Clear clipboard 1

#### Examples
Command -> `clipboards.py switch 1` : Switching to current clipboard<br />
*Clipboard is saved under current id and clipboard doesn't change*

| | Current Clipboard ID | Storage | Clipboard |
|:---:|:---:|:---:|:---:|
| Before | 1 | 1: 123, 2: abc | myclipboard |
| After | 1 | 1: myclipboard, 2: abc | myclipboard |

Command -> `clipboards.py switch 2` : Switching to a different clipboard<br />
*Clipboard is saved under current id, then clipboard 2 is put into the clipboard and the current clipboard is set to 2*

| | Current Clipboard ID | Storage | Clipboard |
|:---:|:---:|:---:|:---:|
| Before | 1 | 1: 123, 2: abc | myclipboard |
| After | 2 | 1: myclipboard, 2: abc | abc |

Command -> `clipboards.py switch 3` : Switching to a clipboard that doesn't exist<br />
*Clipboard is saved under current id and clipboard doesn't change. Clipboard id is 3 and will be created when it is switched next time*

| | Current Clipboard ID | Storage | Clipboard |
|:---:|:---:|:---:|:---:|
| Before | 1 | 1: 123, 2: abc | myclipboard |
| After | 3 | 1: myclipboard, 2: abc | myclipboard |

*Clipboards can be named more than just numbers.*

### Options
* Close GUI when a clipboard is selected - data.json:close_on_gui_select
* Keep window on top until closed - data.json:stay_on_top
* Display HTML as plain text instead of rendering it in the GUI - found in .json:html_as_plain_text
* Opacity of GUI - found in .json:opacity

## Thanks to
* [Michael Robertson](https://github.com/MBRobertson) for adding file support.

## Notes
I have included RunGUI.vbs to be attached to a hot key so the GUI can easily be opened.

## TODO
 - Re-map storage to a sqlite3 database
    - [clipboard (int), type (int), value (bytes)]
    - BLOB for bytes
 - Improve getting clipboard
    - http://timgolden.me.uk/pywin32-docs/win32clipboard.html
 - Replace the refresh with a settings button
 - Migrate settings to the database
 - Put closing the clipboard in a finally so it always occurs
 - Bug: first right click -> view will not open view window (need to pre-create again?)
 - Convert to package format
    - Add setup.py
    - License
    - PyPI?

```python
win32clipboard.OpenClipboard()
format1 = win32clipboard.EnumClipboardFormats()
obj = win32clipboard.GetClipboardData(format1)
print (type(obj))
win32clipboard.CloseClipboard()
```
