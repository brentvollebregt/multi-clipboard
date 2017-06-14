# mutli-clipboard
switch clipboard contents using easily using a command 

The idea of this is to map keys to commands to easily switch contents of your clipboard

Both images and text are supported and unlimited amounts of saved clipboards can be created.

## What This Does
This acts as a hotbar in a game would. When 1 is passed and you are currently using 2 (current is saved in data.json), your clipboard contents will be saved in 2 and 1 will then be loaded; if 1 hasn't been used before, the current clipboard is kept but the data is still saved to 2.

e.g.

1: 123, 2: abc, clipboard: myclipboard

When currently using is 1 and you pass 2:

1: myclipboard, 2: abc, clipboard: abc

## Installation/Setup
1. Install PIL if you are using Python 3 (pip install Pillow)
2. Run the command on main.py passing the index you want to switch

## Notes
I have included windows batch files which could be mapped to keys. I have a keyboard with a "My Favourites" buttons consisting of 1-5. I re-mapped these keys to correspodning commands to switch the current clipboard. This makes it easy to swap my keyboard on the go.
