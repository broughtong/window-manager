import gtk
from configure import *
import pynotify

class wn_system_tray():

    def __init__(self):

        self.tray = None
        self.aboutWindow = None
        self.aboutOpen = False
        self.configureWindow = None
        self.configureOpen = False
        self.daemon = None

        logoLocation = "/home/george/Desktop/wm/wm/logo.png"
        systemTrayName = "Window Manager"

        try:

            import appindicator

            self.tray = appindicator.Indicator(systemTrayName, logoLocation, appindicator.CATEGORY_APPLICATION_STATUS)
            self.tray.set_status(appindicator.STATUS_ACTIVE)

            self.cb_show_menu(None, None, None)
            
        except ImportError as ie:

            try:
                self.tray = gtk.StatusIcon()
                self.tray.set_from_file(logoLocation)
                self.tray.set_tooltip(systemTrayName)
                self.tray.connect('popup-menu', self.cb_show_menu)
                self.tray.connect('activate', self.cb_show_menu, 0, 0)

            except:

                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "The current operating system is not supported: " + e)
                md.set_position(gtk.WIN_POS_CENTER)
                md.run()
                md.destroy()

        gtk.main()

    def cb_show_menu(self, icon, button, time):

        self.menu = gtk.Menu()

        menuItem = gtk.MenuItem("Configure")
        menuItem.connect('activate', self.cb_configure)
        self.menu.append(menuItem)

        menuItem = gtk.MenuItem("Help")
        menuItem.connect('activate', self.cb_help)
        self.menu.append(menuItem)

        menuItem = gtk.MenuItem("About")
        menuItem.connect('activate', self.cb_about)
        self.menu.append(menuItem)

        menuItem = gtk.MenuItem("Exit")
        menuItem.connect('activate', self.cb_exit)
        self.menu.append(menuItem)

        self.menu.show_all()

        try:
            self.tray.set_menu(self.menu)

        except:

            self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.tray)

    def cb_configure(self, widget):

        pass        

    def cb_help(self, widget):

        import webbrowser

        url = "file:///home/george/Desktop/wm/wm/help.html"
        webbrowser.open(url, 2)

    def cb_about(self, widget):

        from about import wn_about

        if self.aboutOpen == False:

            self.aboutOpen = True

            self.aboutWindow = wn_about()
            self.aboutWindow.aboutdialog.run()
            self.aboutWindow.aboutdialog.destroy()

            self.aboutOpen = False

        else:

            import time

            self.aboutWindow.aboutdialog.present_with_time(int(time.time()))
            self.aboutWindow.aboutdialog.window.focus()

    def cb_exit(self, widget):

        if self.aboutOpen == True:

            self.aboutWindow.aboutdialog.destroy()

        gtk.main_quit()
        
    def notification(self, msg):
        try:
            if pynotify.init("My Application Name"):
                Alert = pynotify.Notification("Alert Notification", "A Message From Your Applicaton")
                Alert.show()
            else:
                print "Error starting pynotify"
        except:
            print "pynotify not installed"

