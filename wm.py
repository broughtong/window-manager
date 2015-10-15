import gtk
import pygtk
import keybinder
from ewmh import EWMH
#from Xlib import 
import cairo

keystring = "<Ctrl>F1"

class Rwindow:

    ewmh = EWMH()
    monitors = []
    currentmonitor = 0
    currentmonitoroffset = 0
    startx = 0
    starty = 0
    finishx = 0
    finishy = 0

    def init(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_decorated(False)
        self.window.set_default_size(200, 200)
        self.window.set_size_request(200, 200)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_property("skip-taskbar-hint", True)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.window.connect("destroy", self.cb_delete)
        self.window.connect("delete_event", self.cb_delete)
        self.window.connect("focus_out_event", self.cb_delete)

        self.box = gtk.EventBox()
        self.area = gtk.DrawingArea()
        self.area.connect("expose-event", self.expose_cairo)

        self.box.connect("button-press-event", self.cb_press)
        self.box.connect("button-release-event", self.cb_release)
        self.box.connect("motion_notify_event", self.cb_motion)
        
        self.box.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK)

        self.box.add(self.area)
        self.window.add(self.box)
        self.window.set_keep_above(True)

        self.window.show_all()
        self.window.present()

        self.mouse = 0

        self.start = True
        self.carryx = -20
        self.carryy = -20

    def redraw(self):
        self.dwidget.queue_draw()
        return True

    def expose_cairo(self, widget, event):
        self.dwidget = widget
        self.cr = widget.window.cairo_create()

        self.cr.set_source_rgb(1, 1, 1)
        self.cr.rectangle(0, 0, 200, 200)
        self.cr.fill()

        for i in xrange(0, 6):
            for j in xrange(0, 6):

                self.cr.set_source_rgb(0.6, 0.6, 0.6)
                self.cr.rectangle((30 * i) + 15, (30 * j) + 15, 20, 20)
                self.cr.fill()

        if self.start == False:
            if self.mouse == 0:
                if (((self.carryx - 15) % 30) < 20) and self.carryx < 180:
            
                    if (((self.carryy - 15) % 30) < 20) and self.carryy < 180:

                        self.cr.set_source_rgb(0.3, 0.3, 0.3)
                        self.cr.rectangle(self.carryx - ((self.carryx - 15) % 30), self.carryy - ((self.carryy - 15) % 30), 20, 20)
                        self.cr.fill()
            else:
                mposx = ((self.carryx - ((self.carryx - 15) % 30)) - 15) / 30
                mposy = ((self.carryy - ((self.carryy - 15) % 30)) - 15) / 30

                if mposx > 5:
                    mposx = 5
                if mposy > 5:
                    mposy = 5
                if mposx < 0:
                    mposx = 0
                if mposy < 0:
                    mposy = 0

                x1 = -20
                x2 = -20
                y1 = -20
                y2 = -20
                                
                if self.startx < mposx:
                    x1 = self.startx
                    x2 = mposx
                else:
                    x1 = mposx
                    x2 = self.startx        
                if self.starty < mposy:
                    y1 = self.starty
                    y2 = mposy
                else:
                    y1 = mposy
                    y2 = self.starty

                difx = (x2 - x1) + 1
                dify = (y2 - y1) + 1

                for i in xrange(0, int(difx)):
                    for j in xrange(0, int(dify)):
                        self.cr.set_source_rgb(0.3, 0.3, 0.3)
                        self.cr.rectangle((i * 30) + 15 + (30*x1), (j * 30) + 15 + (30*y1), 20, 20)
                        self.cr.fill()
                
        else:
            self.start = False

    def cb_motion(self, widget, event=0):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state

        self.carryx = x
        self.carryy =y

        self.redraw()

    def cb_delete(self, widget, event=0, data=0):
        gtk.main_quit()
        self.window.destroy()       

    def cb_press(self, box, event, c=0):
        x = event.x
        y = event.y

    
        if (((x - 15) % 30) < 20) and x < 180:
            
            if (((y - 15) % 30) < 20) and y < 180:

                self.mouse = 1
                self.startx = ((x - ((x - 15) % 30)) - 15) / 30
                self.starty = ((y - ((y - 15) % 30)) - 15) / 30

                print self.startx


    def cb_release(self, box, event, c=0):
        x = event.x
        y = event.y

        self.finishx = ((x - ((x - 15) % 30)) - 15) / 30
        self.finishy = ((y - ((y - 15) % 30)) - 15) / 30

        if self.finishx == 6:
            self.finishx = 5
        if self.finishy == 6:
            self.finishy = 5

        if self.finishx == -1:
            self.finishx = 0
        if self.finishy == -1:
            self.finishy = 0


        if self.startx > self.finishx:
            b = self.startx
            self.startx = self.finishx
            self.finishx = b
        if self.starty > self.finishy:
            b = self.starty
            self.starty = self.finishy
            self.finishy = b

        self.cb_delete(0)

    def getDesktopDimensions(self):
        window = gtk.Window()
        screen = window.get_screen()
        nmons = screen.get_n_monitors()
        for m in xrange(nmons):
            mg = [screen.get_monitor_geometry(m).width, screen.get_monitor_geometry(m).height]
            self.monitors.append(mg)
        self.currentmonitor = screen.get_monitor_at_window(screen.get_active_window())
        if self.currentmonitor == 0:
            self.currentmonitoroffset = 0
        else:
            self.currentmonitoroffset = 0
            for i in xrange(0, self.currentmonitor):
                self.currentmonitoroffset += self.monitors[i][0]

    def cb(self,e):
        self.getDesktopDimensions()
        win = self.ewmh.getActiveWindow()

        self.init()
        gtk.main()

        grav = 0

        difx = (self.finishx - self.startx) + 1
        dify = (self.finishy - self.starty) + 1

        self.ewmh.setMoveResizeWindow(win, grav, int(self.currentmonitoroffset + ((self.monitors[self.currentmonitor][0] - 45) / 6 * self.startx)) + 45, int((self.monitors[self.currentmonitor][1] - 24) / 6 * self.starty) + 24, int(self.monitors[self.currentmonitor][0] / 6 * difx), int(self.monitors[self.currentmonitor][1] / 6 * dify))

        self.ewmh.display.flush()

def main():
    rwindow = Rwindow()

    keybinder.bind(keystring, rwindow.cb, "Keystring %s (user data)" % keystring)
    gtk.main()

if __name__ == '__main__':
    main()
