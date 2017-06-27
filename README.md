# mutli-clipboard
switch clipboard contents using easily using a command 

The idea of this is to easily switch keyboards with simple commands. Map commands to keys to use this easily.

Images and text are supported and unlimited amounts of saved clipboards can be created.

## What This Does
This acts as a hotbar in a game would. When 1 is passed and you are currently using 2 (current is saved in data.json), your clipboard contents will be saved in 2 and 1 will then be loaded; if 1 hasn't been used before, the current clipboard is kept but the data is still saved to 2.

e.g.<br />
1: 123, 2: abc, clipboard: myclipboard<br />
When currently using is 1 and you pass 2:<br />
1: myclipboard, 2: abc, clipboard: abc

Clipboards can be named more than just numbers.

## Installation/Setup
1. Install PIL if you are using Python 3 (pip install Pillow)
2. Install PYQT5 (pip install pyqt5)
2. Run the command on clipboards.py

## Usage
* clipboards.py switch clipboard - Will switch current clipboard to the clipboard specified
* clipboards.py clear - Clear all clipboards
* clipboards.py clear 1 - Clear clipboard 1
* clipboards.py view - View all clipboards (opens GUI)
* clipboards.py view 1 - Views clipboard 1

## Still in Development
The GUI is still in development and currently will only display the frame, to close you can use the close button on the bottom right. In the future this will display all cipboards and here you will be able to switch between them easily without a command.