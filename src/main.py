import os
from daemon import *

if __name__ == "__main__":

	if os.geteuid() != 0:

		daemon = wn_daemon()

	else:

		print "Script must NOT be run as root"
