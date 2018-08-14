import clipboard
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


def delete_stored_clipboards(db_manager, clipboard_ids):
    """ Takes a list of clipboards to be deleted, will make sure there is still a clipboard left """

    # Delete all clipboards requested
    for clipboard_id in clipboard_ids:
        db_manager.remove_clipboard(clipboard_id)

    # If there are no more clipboards left, set the current clipboard to 0 and put the users clipboard into it
    if len(db_manager.get_clipboard_ids()) < 1:
        db_manager.current_clipboard = 0
        store_clipboard(db_manager)


def store_clipboard(db_manager):
    """ Stores the users current clipboard into the current clipboard in the database """
    user_clipboard_type = clipboard.get_clipboard_type()
    user_clipboard_contents = clipboard.get_clipboard()
    user_clipboard_preview = clipboard.get_clipboard_preview()
    current_clipboard_id = db_manager.current_clipboard
    db_manager.set_clipboard(current_clipboard_id, user_clipboard_type, user_clipboard_contents, user_clipboard_preview)


def set_clipboard(db_manager, clipboard_id):
    """ Puts a stored clipboard on the clipboard """
    requested_clipboard = db_manager.get_clipboard(clipboard_id)
    clipboard.set_clipboard(requested_clipboard['type'], requested_clipboard['content'])
    db_manager.current_clipboard = clipboard_id
