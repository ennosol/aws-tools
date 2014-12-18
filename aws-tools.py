#!/usr/bin/python
# ---------------------------------------------------------
# AWS Security Group Syncronization by IP address
#
# @author Peter Perger @ Ennosol Technology Co. Ltd.
# @package aws-tools
# ---------------------------------------------------------

import sys
import os
import colorization
import wlo
import aws

# Check Pip and AWS CLI
wlo.checkPythonPackage("pip")
wlo.checkPipPackage("awscli")
colorization.info("AWS CLI OK")

# Check credentials and config file
aws.checkCredentials()

# Check command
if (len(sys.argv) == 1):
    colorization.err("Wrong argument! (usage: ./aws-toolkit.py <command> [options])")
    sys.exit()

# Sync IP address in security group
if (sys.argv[1] == "syncip"):
    # Check group id
    if (len(sys.argv) == 2):
        colorization.err("Wrong argument! (usage: ./aws-toolkit.py syncip <group id>)")
        sys.exit()
    else:
        aws.syncIp(sys.argv[2])
        sys.exit()
        
# Sync IP addresses between groups
# TODO

# Wrong command
colorization.err("Wrong command! (usage: ./aws-toolkit.py <command> [options])")
sys.exit()


