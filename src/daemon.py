import keybinder
import gtk

from resize import *
from systemtray import * 

class wn_daemon():

    def __init__(self):

        self.keystring = "<Ctrl><Shift>"
        self.bind()

        self.window = None

        self.systemtray = wn_system_tray()

    def cb_hotkey(self, e):

        if self.window == None:

            self.window = wn_resize()

        else:

            if self.window.isOpen == False:

                self.window = wn_resize()    

    def bind(self):

        try:
            if keybinder.bind(self.keystring, self.cb_hotkey, None):

                pass

            else:

                raise KeyError('Failed to bind')

        except KeyError as e:

            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "Failed to bind key, check that it is not already being used")
            md.set_position(gtk.WIN_POS_CENTER)
            md.run()
            md.destroy()

    def unbind(self):

        try:

            keybinder.unbind(self.keystring)

        except:

            pass

    def rebind(self, newKeyString):

        self.unbind()
        self.keystring = newKeyString
        self.bind()
