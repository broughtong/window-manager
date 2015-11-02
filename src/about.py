import gtk

class wn_about():

    def __init__(self):

        self.aboutdialog = gtk.AboutDialog()
        self.aboutdialog.set_position(gtk.WIN_POS_CENTER)
        self.aboutdialog.set_name("Window Manager")
        self.aboutdialog.set_version("0.01")
        self.aboutdialog.set_comments("Desktop Window Manager")
        self.aboutdialog.set_authors(["Written by\n\nGeorge Broughton\nPeter Lightbody"])
