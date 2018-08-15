from db import DatabaseManager
import ui
import listener
import utils
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--set', type=int, action='store', help='set the current clipboard')
parser.add_argument('-c', '--clear', type=utils.check_clear_arg, action='append', help='clear a clipboard')
parser.add_argument('--start-listener', help='start the listener', action='store_true')
parser.add_argument('--stop-listener', help='stop the listener if it is running', action='store_true')
parser.add_argument('--current', help='get the current clipboard the user is on', action='store_true')
args = parser.parse_args()

db_manager = DatabaseManager()

utils.store_clipboard(db_manager)

if args.clear is None and args.set is None and not args.start_listener and not args.stop_listener and args.current is None:
    # If there were no arguments passed, open the UI
    ui.show_clipboard_selector(db_manager)

if args.set is not None:
    stored_clipboard_data = db_manager.get_clipboard(args.set)
    if stored_clipboard_data is None:
        # If the requested clipboard id doesn't exist: put the users clipboard in the new clipboard (don't touch old)
        db_manager.current_clipboard = args.set
        utils.store_clipboard(db_manager)
        print ('Clipboard switched to ' + str(args.set))
        print ('This clipboard did not exist so your clipboard was not changed')
    else:
        # If the requested clipboard id does exist: load the clipboard data
        utils.set_clipboard(db_manager, args.set)
        print ('Clipboard switched to ' + str(args.set))
        print ('Data from clipboard ' + str(args.set) + ' has been loaded into your clipboard')

if args.clear is not None and len(args.clear) > 0:
    clipboard_ids = args.clear
    if '*' in args.clear:
        # If * is passed, get all the clipboards to be deleted
        clipboard_ids = db_manager.get_clipboard_ids()

    utils.delete_stored_clipboards(db_manager, clipboard_ids)

    if '*' in args.clear:
        print ('All clipboard cleared')
        print ('You are now on clipboard 0')
    else:
        print('Clipboards ' + str(args.clear) + 'cleared')
        if db_manager.current_clipboard in args.clear:
            print ('Clipboard ' + str(db_manager.current_clipboard) + ' will be re-created as you are currently on it')

if args.start_listener:
    # If --start-listener is passed, start the listener
    if not listener.is_listener_running():
        listener.start_listener()
        print('Listener has been started')
    else:
        print ('Listener is already running')

if args.stop_listener:
    # If --stop-listener is passed, stop the listener
    if listener.is_listener_running():
        listener.stop_listener()
        print ('Listener has been stopped')
    else:
        print('Listener isn\'t running')

if args.current:
    # Show the user what clipboard they are currently on
    print ('Currently you are on clipboard ' + str(db_manager.current_clipboard))
