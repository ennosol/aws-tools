#!/usr/bin/python
# ---------------------------------------------------------
#
# WLO (Windows, Linux, OS X) helper functions
#
# @author Peter Perger @ Ennosol Technology Co. Ltd.
# @package aws-tools
#
# ---------------------------------------------------------

import sys
import os
import socket
import colorization
from os.path import expanduser

# Linux OS
if (sys.platform == "linux2"):

    def checkPythonPackage(package):
        if not os.popen("ls /usr/local/lib/python2.7/dist-packages/ | grep %s 2>/dev/null" % package):
            colorization.err("Python package '%s' not found" % package)
            sys.exit()

    def checkPipPackage(package):
        if not os.popen("pip list | grep %s 2>/dev/null" % package):
            colorization.err("Pip package '%s' not found" % package)
            sys.exit()

    def getIPAddress():
        return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    def getHome():
        return expanduser("~")
        
# Windows OS
elif (sys.platform == "win32"):
    colorization.err("Missing helper functions!");
    sys.exit()

# Mac OS X OS
elif (sys.platform == "darwin"):
    colorization.err("Missing helper functions!");
    sys.exit()

# Other
else:
    colorization.err("Missing helper functions!");
    sys.exit()

