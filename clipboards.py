import clipboard_assist
import sys
import os

clipboards_location = os.getcwd() + "/clipboards/"
data = clipboard_assist.getData()

if len(sys.argv) < 2:
    print ("Usage: python clipboards.py {switch, clear, view}")
    exit()

if sys.argv[1] == "switch":
    if len(sys.argv) == 3:
        clipboard = clipboard_assist.cleanString(sys.argv[2])
        clipboard_assist.saveClipboard(clipboards_location, data)
        clipboard_assist.loadClipboard(clipboards_location, clipboard)
        data["current_clipboard"] = clipboard
        clipboard_assist.setData(data)
    else:
        print ("Usage: python clipboards.py switch clipboard")

elif sys.argv[1] == "clear":
    if len(sys.argv) == 2:
        for clipboard in os.listdir(clipboards_location):
            clipboard_assist.clear(clipboards_location, clipboard[:-4])
        data["current_clipboard"] = '1'
        clipboard_assist.setData(data)
    elif len(sys.argv) == 3:
        clipboard = clipboard_assist.cleanString(sys.argv[2])
        if not clipboard_assist.clear(clipboards_location, clipboard):
            print ("Clipboard " + clipboard + " does not exist")
    else:
        print ("Usage: python clipboards.py clear [clipboard]")

elif sys.argv[1] == "view":
    if len(sys.argv) == 2:
        clipboard_assist.view(clipboards_location)
    elif len(sys.argv) == 3:
        if not clipboard_assist.view_single(clipboards_location, sys.argv[2]):
            print ("Clipboard " + sys.argv[2] + " does not exist")
    else:
        print ("Usage: python clipboards.py view [clipboard]")

else:
    print ("Usage: python clipboards.py {switch, clear, view}")
