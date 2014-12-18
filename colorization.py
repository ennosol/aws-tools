#!/usr/bin/python
# ---------------------------------------------------------
#
# Colorization
#
# @author Peter Perger @ Ennosol Technology Co. Ltd.
# @package aws-tools
#
# ---------------------------------------------------------

# Defined colors
c_info="\033[0;36m"     # Cyan
c_ok="\033[0;32m"       # Green
c_err="\033[0;31m"      # Red
c_warn="\033[0;33m"     # Orange
c_colorend="\033[0m"

# Print colorized message
def c_print(color,msg):
    print '%s%s%s' %(color,msg,c_colorend)
    
def info(msg):
    c_print(c_info,msg)
def ok(msg):
    c_print(c_ok,msg)
def warn(msg):
    c_print(c_warn,msg)
def err(msg):
    c_print(c_err,msg)
    
