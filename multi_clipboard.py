from db import DatabaseManager
import clipboard
import ui

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--set', action='store', help='set the current clipboard')
parser.add_argument('-c', '--clear', action='append', help='clear a clipboard') # TODO Allow * to delete all
parser.add_argument('--start-listener', help='start the listener', action='store_true')
parser.add_argument('--stop-listener', help='stop the listener if it is running', action='store_true')

args = parser.parse_args()

db_manager = DatabaseManager()

if len(args.clear) == 0 and args.set is None and not args.start_listener and not args.stop_listener:
    # TODO Open UI
    pass

if args.set is not None:
    # TODO Set clipboard
    # Check if we can deal with clipboard -> clipboard.get_clipboard_type() is not None
    pass

if len(args.clear) > 0:
    # TODO Clear clipboards
    pass

if args.start_listener:
    # TODO Stop listener
    pass

if args.stop_listener:
    # TODO Start listener
    pass



# TODO Check if we can handle the clipboard


# TODO Just calling the script will open the UI
# TODO --start-listener + --stop-listener
# TODO Manually change clipboards -set 0
# TODO Manually clear a clipboard -clear 0
