#!/usr/bin/python
# ---------------------------------------------------------
#
# AWS helper functions
#
# @author Peter Perger @ Ennosol Technology Co. Ltd.
# @package aws-tools
#
# ---------------------------------------------------------

import os
import json
import wlo
import colorization

# AWS files
HOME = wlo.getHome()
AWS_CREDENTIALS = HOME + "/.aws/credentials"
AWS_CONFIG = HOME + "/.aws/config"

# Check credentials and config file
def checkCredentials():
    # Check AWS credentials
    if not os.path.isfile(AWS_CREDENTIALS):
        colorization.warn("Credentials (%s) not found. Please type your credentials: " % AWS_CREDENTIALS)
        aws_access_key_id = raw_input("Access Key ID: ")
        aws_secret_access_key = raw_input("Secret Access Key: ")
        f = open(AWS_CREDENTIALS, 'w')
        f.write('[default]\naws_access_key_id=%s\naws_secret_access_key=%s\n' %(aws_access_key_id, aws_secret_access_key))
        f.close()
    colorization.info("Credentials OK.")
    # Check AWS config
    if not os.path.isfile(AWS_CONFIG):
        colorization.warn("Config (%s) not found. Please type your region: " % AWS_CONFIG)
        region = raw_input("Region: ")
        print "Output: json"
        f = open(AWS_CONFIG, 'w')
        f.write('[default]\nregion=%s\noutput=json\n' % region)
        f.close()
    colorization.info("Config OK.")

# Get security group details
def getSecGroup(group_id):
    return json.load(os.popen("aws ec2 describe-security-groups --group-ids %s" % group_id))
    
# Remove IP address from security group
def removeIPFromSecGroup(group_id, ip):
    os.system("aws ec2 revoke-security-group-ingress --group-id %s --protocol tcp --port 22 --cidr %s/32 > /dev/null 2>&1" % (group_id, ip))
    
# Add IP address to AWS SG
def addIPToSecGroup(group_id, ip):
    os.popen("aws ec2 authorize-security-group-ingress --group-id %s --protocol tcp --port 22 --cidr %s/32" % (group_id, ip))

# Check IP address in security group    
def checkIPAddressInSecGroup(group_id, ip, info=False):
    data = getSecGroup(group_id)
    if info: print data["SecurityGroups"][0]["GroupName"]
    for permission in data["SecurityGroups"][0]["IpPermissions"]:
        if (("ToPort" in permission) and ("IpProtocol" in permission) and ("UserIdGroupPairs" in permission) and ("IpRanges" in permission) and 
            (permission["ToPort"] == 22) and (permission["IpProtocol"] == 'tcp') and (not permission["UserIdGroupPairs"])):
            for iprange in permission["IpRanges"]:
                # print iprange["CidrIp"]
                if (iprange["CidrIp"].split("/").pop(0) == ip):
                    return True

# Sync IP address in security group
def syncIp(group_id):
    # Get IP address
    ip = wlo.getIPAddress()
    colorization.ok("Your IP: %s" % ip)
    # Previous IP address and log
    ip_old = ""
    ip_log = HOME + "/.aws/ip.log"
    # Check and read old IP address
    if os.path.isfile(ip_log):
        with open(ip_log, "r") as log:
            ip_old = log.read().replace('\n', '')
            colorization.info("Old IP: %s" % ip_old)
    # Check IP address in AWS SG
    if not checkIPAddressInSecGroup(group_id, ip, True):
        colorization.warn("This security group does not contain your IP address")
        # Remove IP address from AWS SG
        removeIPFromSecGroup(group_id, ip_old)
        print "Old IP address removed from this security group"
        # Add IP address to AWS SG
        addIPToSecGroup(group_id, ip)
        print "New IP address added to this security group"
        # Check IP address in AWS SG
        if (checkIPAddressInSecGroup(group_id, ip) == True):
            colorization.ok("This security group contains your IP address")
            f = open(ip_log,'w')
            f.write(ip)
            f.close()
        else:
            colorization.err("This security group does not contain your IP address")
    else:
        colorization.ok("This security group contains your IP address")

    
    
    
    
