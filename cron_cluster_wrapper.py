#!/usr/bin/env python
# cron_cluster_wrapper.py
"""
This is a wrapper that is cluster-aware for cronjobs.

it runs clustat and based on the output, finds cluster members and what 
services are running on that node.  the argument --service specifies the
service that is important to this cronjob.  If the member, as provided
by --node (this should be set to $HOSTNAME or something similar), 
is running the service, then the wrapper will execute the --script 


Example:

##### in crontab:
0 2 0 0 0 /usr/local/sbin/cron_cluster_wrapper.py --node thishost --service mysql --script=/usr/local/sbin/myscript.sh 


"""
# 

import os
import subprocess
import re
import logging
import optparse

logging.basicConfig (level=logging.INFO, 
					 format='%(asctime)s %(levelname)s %(message)s')

cmd_clustat='/usr/sbin/clustat'


def grab_clustat_output():
	""" 
	this runs clustat and returns the output in a list.  from there, deal with it.
	"""
	p = subprocess.Popen('/usr/sbin/clustat',stdout=subprocess.PIPE).stdout
	return p.readlines()


def find_cluster_members(clustat_output):
	"""finds the list of cluster members"""
	# regular expression: Online, match, and grab first element in row, check to see if Local is there too


	for line in clustat_output:
		localmatch = re.search('.*(?=[0-9] Online.*Local.*)', line)
		match = re.search('.*(?=[0-9] Online)', line)
		if localmatch is not None:
			print "LOCAL: %s" % localmatch.group(0)
		elif match is not None:
			print " %s " % match.group(0)


#  this does the trick, but ugly.
for line in m:
	localmatch = re.search('.*(?=[0-9] Online.*Local.*)', line)
	match = re.search('.*(?=[0-9] Online)', line)
	if localmatch is not None:
		print "LOCAL: %s -" % localmatch.group(0)
	elif match is not None:
		print " %s -" % match.group(0)

# this does the trick better, but not WELL - we can't get the second capture for some reason.  Gotta figure that out
for line in m:
	match = re.search('^ ([A-Za-z0-9_-]+).*Online.*(Local)?.*', line)
	match.groups()
	if match is not None:
		print " %s ;" % [match.group(1,2)]


	pass


def main():
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)

	parser.add_option



	pass
