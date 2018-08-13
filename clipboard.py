import win32clipboard

CF_IMAGES = win32clipboard.CF_DIBV5
CF_FILES = 49376
CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
CF_UNICODE_TEXT = win32clipboard.CF_UNICODETEXT
CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
CF_PLAIN_TEXT = win32clipboard.CF_TEXT

# Store the supported formats in order they must be read in
SUPPORTED_CF = [
    # 49384, # 49384: Focus on publisher items # TODO Find something that won't influence the rest - we already had it?
    CF_IMAGES, # 17: Images
    CF_FILES, # 49376: Files/Folders
    CF_HTML, # 49384: HTML
    CF_UNICODE_TEXT, # 13: Unicode Text
    CF_RTF, # 49285: Rich text
    CF_PLAIN_TEXT # 1: Text
]


def get_clipboard_type():
    """ Get the most recommended clipboard format, return None if we can't handle it """
    win32clipboard.OpenClipboard()
    supported_cf = None
    for _format in SUPPORTED_CF:
        if win32clipboard.IsClipboardFormatAvailable(_format):
            supported_cf = _format
            break
    win32clipboard.CloseClipboard()
    return supported_cf


def get_clipboard():
    """ Return the current data in the clipboard """
    format_available = get_clipboard_type()
    win32clipboard.OpenClipboard()
    contents = win32clipboard.GetClipboardData(format_available)
    win32clipboard.CloseClipboard()
    return contents


def set_clipboard(_type, _data):
    """ Set the clipboard passing a format (type) and data """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(_type, _data)
    win32clipboard.CloseClipboard()
