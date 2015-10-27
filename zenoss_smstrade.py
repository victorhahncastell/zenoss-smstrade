#! /usr/bin/env python
# ============================== SUMMARY =====================================
#
# Program : zenoss_smstrade.py
# Version : 1.0
# Author : Victor Hahn Castell <victor@hahncastell.de>
# Summary : Script to use the smstrade.de HTTP API as pager/SMS notification provider in Zenoss.
#           Based on a similar script for smseagle.eu
# Copyright (c) 2015 Victor Hahn Castell
#               2013 The SMSEagle Team
# License : BSD


import os
import sys
import time
import urllib
import urllib2

# Edit these settings to match your own
APIKEY = "schluesselolometer"
LOG_ENABLED = 1


def main():

    try:
       	# Read recipient number
        apikey = sys.argv[1]
        rcpt = sys.argv[2]
        route = sys.argv[3]

        sender = None
        if len(sys.argv) > 3:
          sender = sys.argv[4]
        else:
          sender = "Zenoss"

        debug = 0
        if len(sys.argv) > 4:
          debug = sys.argv[5]

        log_enabled = False
        if len(sys.argv) > 5:
          log_enabled = sys.argv[6]

    except:
        print "Invalid arguments! Usage: zenoss_smstrade <API key> <recipient> <route> [from] [debug] [log]"
        print "API KEY: your personal key as assigned by smstrade"
        print "Recipient: Recipient's cell number"
        print "Route: One of basic, gold, direct -- refer to smstrade website"
        print "From: Sender information (max 11 characters or 16 digits)"
        print "Debug: If set to 1, tell the smstrade API we're just testing and don't want to really send SMS."
        print "Log: Set to 1 to log to [ZENHOME]/log/smstrade.log"
        sys.exit(1)

    try:
        # Open logfile if logging enabled
        if log_enabled == "1":
            file = os.environ['ZENHOME']+"/log/sms_smstrade.log"
            log = open(file, 'a')
    except:
        print "Cannot open log file!"
        sys.exit(2)

    try:
       	# Read message from standard in
       	msg = sys.stdin.read()

       	# Prepare HTTP request
       	base_url = "http://gateway.smstrade.de/"
       	query_args = { 'key': apikey,
                       'route': route,
                       'to': rcpt,
                       'message': msg,
                       'from': sender,
                       'debug': debug}
       	encoded_args = urllib.urlencode(query_args)
       	url = base_url + '?' + encoded_args

       	# Write log if logging enabled
       	if log_enabled == "1":
       	    timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
       	    log.write("%s ===== BEGIN SENDING SMS ==== \n" % timestamp)
       	    log.write("%s SMS recipient: %s\n" % (timestamp, rcpt))
       	    log.write("%s SMS text: %s\n" % (timestamp, msg))
            log.write("%s API URL: %s\n" % (timestamp, url))

       	#HTTP request to SMStrade
       	result = urllib2.urlopen(url).read()

        # Write log if logging enabled
        if log_enabled  == "1":
            timestamp = "["+time.strftime("%Y-%m-%d %H:%M:%S")+"]"
            try:
                log.write("%s Sending result: %s\n" % (timestamp, result))
                log.write("%s ===== END SENDING SMS ====\n" % timestamp)
            finally:
                log.close()

        resultcode = result.split('\n')[0]
        if resultcode != "100":
          print resultcode
          print "Smstrade did not acknowledge SMS sent; see smstrade documentation for meaning of error code above."

    except Exception, e:
        print e
        sys.exit(1)


main()
