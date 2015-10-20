import os
from systemtray import *

if __name__ == "__main__":

	if os.geteuid() != 0:

		systemTray = wn_system_tray()

		if systemTray.tray != None:
			gtk.main()

	else:

		print "Script must NOT be run as root"
