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
    wNum = 8
    hNum = 8
    windowSize = 400
    windowBoxSize = 30
    windowSpacesize = 40
    margin = 15


    def init(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_decorated(False)
        self.window.set_default_size(self.windowSize,self.windowSize)
        self.window.set_size_request(self.windowSize, self.windowSize)
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

        self.mouse = False

        self.start = True
        self.mousePoseX = -self.windowBoxSize
        self.mousePoseY = -self.windowBoxSize

    def redraw(self):
        self.dwidget.queue_draw()
        return True

    def expose_cairo(self, widget, event):
        self.dwidget = widget
        self.cr = widget.window.cairo_create()

        self.cr.set_source_rgb(1, 1, 1)
        self.cr.rectangle(0, 0, self.windowSize, self.windowSize)
        self.cr.fill()

        for i in xrange(0, self.wNum):
            for j in xrange(0, self.hNum):

                self.cr.set_source_rgb(0.6, 0.6, 0.6)
                self.cr.rectangle((self.windowSpacesize * i) + self.windowSpacesize, (self.windowSpacesize * j) + self.windowSpacesize, self.windowBoxSize, self.windowBoxSize)
                self.cr.fill()

        if not self.start:
            if not self.mouse:
                if (((self.mousePoseX - self.windowSpacesize) % self.windowSpacesize) < self.windowBoxSize) and self.mousePoseX < self.windowSize - self.margin:
            
                    if (((self.mousePoseY - self.windowSpacesize) % self.windowSpacesize) < self.windowBoxSize) and self.mousePoseY < self.hNum - self.margin:

                        self.cr.set_source_rgb(0.3, 0.3, 0.3)
                        self.cr.rectangle(self.mousePoseX - ((self.mousePoseX - self.windowSpacesize) % self.windowSpacesize), self.mousePoseY - ((self.mousePoseY - self.windowSpacesize) % self.windowSpacesize), self.windowBoxSize, self.windowBoxSize)
                        self.cr.fill()
            else:
                mposx = ((self.mousePoseX - ((self.mousePoseX - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize
                mposy = ((self.mousePoseY - ((self.mousePoseY - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize

                if mposx > self.wNum-1:
                    mposx = self.wNum-1
                if mposy > self.hNum-1:
                    mposy = self.hNum-1
                if mposx < 0:
                    mposx = 0
                if mposy < 0:
                    mposy = 0

                x1 = -self.windowBoxSize
                x2 = -self.windowBoxSize
                y1 = -self.windowBoxSize
                y2 = -self.windowBoxSize
                                
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
                        self.cr.rectangle((i * self.windowSpacesize) + self.windowSpacesize + (self.windowSpacesize*x1), (j * self.windowSpacesize) + self.windowSpacesize + (self.windowSpacesize*y1), self.windowBoxSize, self.windowBoxSize)
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

        self.mousePoseX = x
        self.mousePoseY =y

        self.redraw()

    def cb_delete(self, widget, event=0, data=0):
        gtk.main_quit()
        self.window.destroy()       

    def cb_press(self, box, event, c=0):
        x = event.x
        y = event.y

    
        if (((x - self.windowSpacesize) % self.windowSpacesize) < self.windowBoxSize) and x < self.windowSize-self.margin:
            
            if (((y - self.windowSpacesize) % self.windowSpacesize) < self.windowBoxSize) and y < self.windowSize-self.margin:

                self.mouse = True
                self.startx = ((x - ((x - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize
                self.starty = ((y - ((y - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize

    def cb_release(self, box, event, c=0):
        x = event.x
        y = event.y

        self.finishx = ((x - ((x - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize
        self.finishy = ((y - ((y - self.windowSpacesize) % self.windowSpacesize)) - self.windowSpacesize) / self.windowSpacesize

        if self.finishx == self.wNum:
            self.finishx = self.wNum-1
        if self.finishy == self.hNum:
            self.finishy = self.hNum-1

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

        self.ewmh.setMoveResizeWindow(win, grav, int(self.currentmonitoroffset + ((self.monitors[self.currentmonitor][0] - 45) / self.wNum * self.startx)) + 45, int((self.monitors[self.currentmonitor][1] - 24) / self.hNum * self.starty) + 24, int(self.monitors[self.currentmonitor][0] / self.wNum * difx), int(self.monitors[self.currentmonitor][1] / self.hNum * dify))

        self.ewmh.display.flush()

def main():
    rwindow = Rwindow()

    keybinder.bind(keystring, rwindow.cb, "Keystring %s (user data)" % keystring)
    gtk.main()

if __name__ == '__main__':
    main()
