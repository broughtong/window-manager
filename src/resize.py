import gtk
import pygtk
import keybinder
import cairo

from ewmh import EWMH

class wn_resize():

	def __init__(self):

		self.mousePressed = False
		self.startX = -1
		self.startY = -1
		self.isOpen = True
		self.nBoxesW = 6
		self.nBoxesH = 6
		self.windowSpaceSizeW = 30
		self.windowSpaceSizeH = 30
		self.windowBoxSizeW = 20
		self.windowBoxSizeH = 20
		self.margin = 25
		self.windowSizeW = 220
		self.windowSizeH = 220
		self.mPosX = -self.windowBoxSizeW
		self.mPosY = -self.windowBoxSizeH

		self.ewmh = EWMH()
		self.activeWindow = self.ewmh.getActiveWindow()
		if self.activeWindow == self.ewmh.getClientListStacking()[0]:
			return
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		self.window.set_decorated(False)
		self.window.set_default_size(self.windowSizeW,self.windowSizeH)
		self.window.set_size_request(self.windowSizeW, self.windowSizeH)
		self.window.set_resizable(False)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_property("skip-taskbar-hint", True)
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

		self.cr.set_source_rgb(1, 1, 1)
		self.cr.rectangle(0, 0, self.windowSizeW, self.windowSizeH)
		self.cr.fill()

		for i in xrange(0, self.nBoxesW):
			for j in xrange(0, self.nBoxesH):

				self.cr.set_source_rgb(0.6, 0.6, 0.6)
				self.cr.rectangle((self.windowSpaceSizeW * i) + self.margin, (self.windowSpaceSizeH * j) + self.margin, self.windowBoxSizeW, self.windowBoxSizeH)
				self.cr.fill()

		if not self.mousePressed:

			if (self.mPosX - self.margin) % self.windowSpaceSizeW < self.windowBoxSizeW and self.mPosX < self.windowSizeW - self.margin and self.mPosX > self.margin:
				if (self.mPosY - self.margin) % self.windowSpaceSizeH < self.windowBoxSizeH and self.mPosY < self.windowSizeH - self.margin and self.mPosY > self.margin:

					self.cr.set_source_rgb(.3, .3, .3)
					self.cr.rectangle(self.mPosX - ((self.mPosX - self.margin) % self.windowSpaceSizeW), self.mPosY - ((self.mPosY - self.margin) % self.windowSpaceSizeH), self.windowBoxSizeW, self.windowBoxSizeH)
					self.cr.fill()

		else:

			x1 = self.startX
			y1 = self.startY
			x2 = ((self.mPosX - ((self.mPosX - self.margin) % self.windowSpaceSizeW)) - self.margin) / self.windowSpaceSizeW 
			y2 = ((self.mPosY - ((self.mPosY - self.margin) % self.windowSpaceSizeH)) - self.margin) / self.windowSpaceSizeH

			if x2 < 0:
				x2 = 0
			if y2 < 0:
				y2 = 0
			if x2 > self.nBoxesW - 1:
				x2 = self.nBoxesW - 1
			if y2 > self.nBoxesH - 1:
				y2 = self.nBoxesH - 1

			if x1 > x2:
				x1 = x2
				x2 = self.startX
			if y1 > y2:
				y1 = y2
				y2 = self.startY

			for i in xrange(int(x1), int(x2) + 1):
				for j in xrange(int(y1), int(y2) + 1):
					self.cr.set_source_rgb(0.3, 0.3, 0.3)
					self.cr.rectangle((i * self.windowSpaceSizeW) + self.margin, (j * self.windowSpaceSizeH) + self.margin, self.windowBoxSizeW, self.windowBoxSizeH)
				        self.cr.fill()
	def redraw(self):

		self.cairoWidget.queue_draw()

	def cb_destroy(self, widget=None, event=None):

		self.window.destroy()
		self.isOpen = False

	def cb_press(self, widget=None, event=None):

		self.mPosX = event.x
		self.mPosY = event.y

		if (self.mPosX - self.margin) % self.windowSpaceSizeW < self.windowBoxSizeW and self.mPosX < self.windowSizeW - self.margin and self.mPosX > self.margin:
			if (self.mPosY - self.margin) % self.windowSpaceSizeH < self.windowBoxSizeH and self.mPosY < self.windowSizeH - self.margin and self.mPosY > self.margin:

				self.mousePressed = True
				self.startX = int((self.mPosX - self.margin) / self.windowSpaceSizeW)
				self.startY = int((self.mPosY - self.margin) / self.windowSpaceSizeH)

	def cb_release(self, widget=None, event=None):

		x1 = self.startX
		y1 = self.startY

		if x1 < 0 or y1 < 0:
			return

		x2 = ((event.x - ((event.x - self.margin) % self.windowSpaceSizeW)) - self.margin) / self.windowSpaceSizeW 
		y2 = ((event.y - ((event.y - self.margin) % self.windowSpaceSizeH)) - self.margin) / self.windowSpaceSizeH

		if x2 < 0:
			x2 = 0
		if y2 < 0:
			y2 = 0

		if x2 > self.nBoxesW - 1:
			x2 = self.nBoxesW - 1
		if y2 > self.nBoxesH - 1:
			y2 = self.nBoxesH - 1
		if x1 > x2:
			x1 = x2
			x2 = self.startX
		if y1 > y2:
			y1 = y2
			y2 = self.startY

		self.resize(x1, y1, x2, y2)	

		self.cb_destroy()

	def getDesktopDimensions(self):

		window = gtk.Window()
		screen = window.get_screen()
		nMonitors = screen.get_n_monitors()
		lMonitors = []
		self.offset = 0

		for i in xrange(0, nMonitors):
			lMonitors.append([screen.get_monitor_geometry(i).width, screen.get_monitor_geometry(i).height])

		currentMonitorIndex = screen.get_monitor_at_window(screen.get_active_window())

		if currentMonitorIndex != 0:
			for i in xrange(0, currentMonitorIndex):
				self.offset += lMonitors[i][0]

		return lMonitors[currentMonitorIndex][0], lMonitors[currentMonitorIndex][1]

	def resize(self, x1, y1, x2, y2):

		grav = 0

		screenDimensions = self.getDesktopDimensions()

		sectionSizeW = screenDimensions[0] / self.nBoxesW
		sectionSizeH = screenDimensions[1] / self.nBoxesH

		xPos = int(screenDimensions[0] / self.nBoxesW * x1)
		yPos = int(screenDimensions[1] / self.nBoxesH * y1)

		width = int(((x2 + 1) - x1) * (screenDimensions[0]) / self.nBoxesW)
		height = int(((y2 + 1) - y1) * (screenDimensions[1]) / self.nBoxesH)

		self.ewmh.setWmState(self.activeWindow, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
		self.ewmh.setWmState(self.activeWindow, 0, '_NET_WM_STATE_MAXIMIZED_VERT')

		self.ewmh.setMoveResizeWindow(self.activeWindow, grav, self.offset + xPos, yPos, width, height)
		self.ewmh.display.flush()

	def cb_motion(self, widget=None, event=None):

		if event.is_hint:

			x, y, state = event.window.get_pointer()

		else:

			x = event.x
			y = event.y
			state = event.state
		
		self.mPosX = x
		self.mPosY = y

		self.redraw()
