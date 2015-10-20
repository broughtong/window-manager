import gtk
import pygtk
import keybinder
import cairo

from ewmh import EWMH

class wn_resize():

	def __init__(self):

		self.windowSize = 300
		self.mousePressed = False
		self.isOpen = True

		self.ewmh = EWMH()
		self.activeWindow = self.ewmh.getActiveWindow()
		if self.activeWindow == self.ewmh.getClientListStacking()[0]:
			return
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		self.window.set_decorated(False)
		self.window.set_default_size(self.windowSize,self.windowSize)
		self.window.set_size_request(self.windowSize, self.windowSize)
		self.window.set_resizable(False)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_property("skip-taskbar-hint", True)
		#self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))???
		self.window.connect("destroy", self.cb_destroy)
		self.window.connect("delete_event", self.cb_destroy)
		self.window.connect("focus_out_event", self.cb_destroy)

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

		gtk.idle_add(self.present)

	def present(self):

		self.window.present()

	def expose_cairo(self, widget=None, event=None):

		self.cairoWidget = widget
		self.cr = widget.window.cairo_create()

	def redraw(self):

		self.cairoWidget.queue_draw()

	def cb_destroy(self, widget=None, event=None):

		self.window.destroy()
		self.isOpen = False

	def cb_press(self, widget=None, event=None):

		self.redraw()

	def cb_release(self, widget=None, event=None):

		self.redraw()

	def cb_motion(self, widget=None, event=None):

		self.redraw()
		
