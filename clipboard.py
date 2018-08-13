import win32clipboard


CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")

SUPPORTED_CF = [
    # 49384, # 49384: Focus on publisher items # TODO Find something that won't influence the rest - we already had it?
    win32clipboard.CF_DIBV5, # 17: Images
    49376, # 49376: Files/Folders
    CF_HTML, # 49384: HTML
    win32clipboard.CF_UNICODETEXT, # 13: Unicode Text
    CF_RTF, # 49285: Rich text
    win32clipboard.CF_TEXT # 1: Text
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
