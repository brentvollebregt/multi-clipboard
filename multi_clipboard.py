from db import DatabaseManager
import clipboard
import ui
import listener
import argparse


def check_clear_arg(value):
    """ Make sure the value passed in with the -c flag is either an integer or star (*) """
    if value == '*':
        return '*'
    else:
        try:
            return int(value)
        except:
            raise argparse.ArgumentTypeError("%s is not an integer or '*'" % value)


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--set', type=int, action='store', help='set the current clipboard')
parser.add_argument('-c', '--clear', type=check_clear_arg, action='append', help='clear a clipboard')
parser.add_argument('--start-listener', help='start the listener', action='store_true')
parser.add_argument('--stop-listener', help='stop the listener if it is running', action='store_true')
args = parser.parse_args()

db_manager = DatabaseManager()

# Put users current clipboard into the database
user_clipboard_type = clipboard.get_clipboard_type()
user_clipboard_contents = clipboard.get_clipboard()
user_clipboard_preview = clipboard.get_clipboard_preview()
current_clipboard_id = db_manager.current_clipboard
db_manager.set_clipboard(current_clipboard_id, user_clipboard_type, user_clipboard_contents, user_clipboard_preview)

if args.clear is None and args.set is None and not args.start_listener and not args.stop_listener:
    # If there were no arguments passed, open the UI
    ui.show_clipboard_selector(db_manager)

if args.set is not None:
    stored_clipboard_data = db_manager.get_clipboard(args.set)
    if stored_clipboard_data is None:
        # If the requested clipboard id doesn't exist: put the users clipboard in the new clipboard (don't touch old)
        user_clipboard_type = clipboard.get_clipboard_type()
        user_clipboard_contents = clipboard.get_clipboard()
        user_clipboard_preview = clipboard.get_clipboard_preview()
        db_manager.set_clipboard(args.set, user_clipboard_type, user_clipboard_contents, user_clipboard_preview)
        db_manager.current_clipboard = args.set
    else:
        # If the requested clipboard id does exist: load the clipboard data
        requested_clipboard = db_manager.get_clipboard(args.set)
        clipboard.set_clipboard(requested_clipboard['type'], requested_clipboard['content'])
        db_manager.current_clipboard = args.set

if args.clear is not None and len(args.clear) > 0:
    if '*' in args.clear:
        # If * is passed, get all the clipboards to be deleted
        args.clear = db_manager.get_clipboard_ids()

    # Delete all clipboards in args.clear
    for clipboard_id in args.clear:
        db_manager.remove_clipboard(clipboard_id)

    # If there are no more clipboards left, set the current clipboard to 0 and put the users clipboard into it
    if len(db_manager.get_clipboard_ids()) < 1:
        user_clipboard_type = clipboard.get_clipboard_type()
        user_clipboard_contents = clipboard.get_clipboard()
        user_clipboard_preview = clipboard.get_clipboard_preview()
        db_manager.set_clipboard(0, user_clipboard_type, user_clipboard_contents, user_clipboard_preview)
        db_manager.current_clipboard = 0

if args.start_listener:
    # If --start-listener is passed, start the listener
    listener.start_listener()

if args.stop_listener:
    # If --stop-listener is passed, stop the listener
    listener.stop_listener()
