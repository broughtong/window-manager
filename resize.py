import gtk
import pygtk
import keybinder
from ewmh import EWMH
#from Xlib import 
import cairo

ewmh = EWMH()

keystring = "<Ctrl>F1"

monitors = []
currentmonitor = 0
currentmonitoroffset = 0
pos = ""

class Rwindow:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_decorated(False)
		self.window.set_default_size(200, 200)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
		self.window.connect("destroy", self.cb_delete)
		self.window.connect("delete_event", self.cb_delete)
		self.window.connect("focus_out_event", self.cb_delete)

		self.box = gtk.EventBox()
		self.area = gtk.DrawingArea()
		self.area.connect("expose-event", self.cb_expose)

		self.box.connect("button-press-event", self.cb_click)
		
		self.box.add(self.area)
		self.window.add(self.box)

		self.window.show_all()
		self.window.present()

	def cb_expose(self, widget, event):

		cr = widget.window.cairo_create()
		cr.set_source_rgb(0.6, 0.6, 0.6)
		cr.rectangle(10, 10, 80, 80)
		cr.fill()

		cr.set_source_rgb(0.6, 0.6, 0.6)
		cr.rectangle(110, 110, 80, 80)
		cr.fill()

		cr.set_source_rgb(0.6, 0.6, 0.6)
		cr.rectangle(10, 110, 80, 80)
		cr.fill()

		cr.set_source_rgb(0.6, 0.6, 0.6)
		cr.rectangle(110, 10, 80, 80)
		cr.fill()

	def cb_delete(self, widget, event=0, data=0):
		
		gtk.main_quit()
		self.window.destroy()		

	def cb_click(self, box, event, c=0):
		global pos
		if event.x < 100:
			if event.y < 100:
				pos =  "top left"
			else:
				pos =  "bottom left"
		else:
			if event.y < 100:
				pos =  "top right"
			else:
				pos =  "bottom right"
		self.cb_delete(0)

	def main(self):
		gtk.main()

def getDesktopDimensions():
	global currentmonitoroffset, currentmonitor, monitors
	window = gtk.Window()
	screen = window.get_screen()
	nmons = screen.get_n_monitors()
	for m in xrange(nmons):
		mg = [screen.get_monitor_geometry(m).width, screen.get_monitor_geometry(m).height]
		monitors.append(mg)
	currentmonitor = screen.get_monitor_at_window(screen.get_active_window())
	if currentmonitor == 0:
		currentmonitoroffset = 0
	else:
		currentmonitoroffset = 0
		for i in xrange(0, currentmonitor):
			currentmonitoroffset += monitors[i][0]
def cb(e):
	global pos

	getDesktopDimensions()
	win = ewmh.getActiveWindow()

	rwindow = Rwindow()
	rwindow.main()

	grav = 0
	if pos == "top left":
		ewmh.setMoveResizeWindow(win, grav, currentmonitoroffset, 24, 800, 500)
	elif pos == "top right":
		ewmh.setMoveResizeWindow(win, grav, currentmonitoroffset + 1000, 24, 800, 500)
	elif pos == "bottom left":
		ewmh.setMoveResizeWindow(win, grav, currentmonitoroffset, 500, 800, 500)
	elif pos == "bottom right":
		ewmh.setMoveResizeWindow(win, grav, currentmonitoroffset + 1000, 500, 800, 500)
	ewmh.display.flush()

def main():

	keybinder.bind(keystring, cb, "Keystring %s (user data)" % keystring)
	gtk.main()

if __name__ == '__main__':
	main()
