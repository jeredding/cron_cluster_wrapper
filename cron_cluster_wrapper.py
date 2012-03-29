#!/usr/bin/env python
# cron_cluster_wrapper.py
"""
This is a wrapper that is cluster-aware for cronjobs.  Two-node clusters.

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

logging.basicConfig ( level=logging.INFO, 
					 format='%(asctime)s %(levelname)s %(message)s' )

#cmd_clustat='/usr/sbin/clustat'
cmd_clustat='./clustat'

def grab_clustat_output( ):
	""" 
	this runs clustat and returns the output in a list.  from there, deal with it.
	"""
	p = subprocess.Popen( '/usr/sbin/clustat',stdout=subprocess.PIPE ).stdout
	return p.readlines( )


def find_cluster_members( clustat_output ):
	"""finds the list of cluster members

		this function moves through the list clustat_output that is the output
		of running the clustat binary in RHEL cluster, and snags cluster
		members based on their Online status.  It finds the node the 
		clustat command is running on by the Local keyword in the output.

		the return value is the dictionary containing the node list. 

		supporting more than 2 node clusters wouldn't be hard, but I'm being lazy.

	"""
	# nodelist: dict providing local and sibling node entries
	nodelist = {}

	for line in clustat_output:
		match = re.search( '^ ([A-Za-z0-9_-]+).*Online, (Local)?.*', line )
		if match.group(2) is not None:
			nodelist['local'] = match.group(1) 
		else:
			nodelist['node']= match.group(1) 

	reuturn nodelist


def main():
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)

	parser.add_option



	pass



