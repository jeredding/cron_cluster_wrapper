#!/usr/bin/env python
# cron_cluster_wrapper.py
# By Erik Redding <erik.redding@txstate.edu>
"""
This is a wrapper that is cluster-aware for cronjobs.  Two-node clusters.

it runs clustat and based on the output, finds cluster members and what 
services are running on that node.  the argument --service specifies the
service that is important to this cronjob.  If this member is running the
service, then the wrapper will return 0, otherwise 1.  

Options:
--service=<svcname>     CASE SENSITIVE!

Example:

##### in crontab:
0 2 0 0 0 /usr/local/sbin/cron_cluster_wrapper.py --service mysql && <your cron script>


"""
# 

import os
import sys
import subprocess
import re
import optparse

cmd_clustat='/usr/sbin/clustat'
#cmd_clustat='./clustat_nonmaster'

def grab_clustat_output( ):
    """ 
    this runs clustat and returns the output in a list.  from there, deal with it.
    """
    p = subprocess.Popen( cmd_clustat ,stdout=subprocess.PIPE ).stdout
    return p.readlines( )

def find_cluster_members( clustat_output ):
    """
    finds the list of cluster members

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
        if match is not None:
            if match.group(2) is not None:
                nodelist['local'] = match.group(1) 
            else:
                nodelist['node']= match.group(1) 
    return nodelist

def is_service_running(service, thishost, clustat_output ):
    """
    finds if service is running based on clustat_output list
    """
    for line in clustat_output:
        match = re.search( '^ service:(%s)[ ]+(%s)[ ]+(started).*' % ( service, thishost ) , line )
        if match is not None:
            # MATCH! Lets return True.
            return True
    # We didn't find it.  Return False!
    return False

def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-s", "--service", action="store",
                      help="service name")
    opts, ____ = parser.parse_args()

    # run clustat, get output
    output=grab_clustat_output()
    # give output to find our cluster members
    cluster_members=find_cluster_members(output)

    # if the service is running, on the local node, pass the output and script will:
    if is_service_running( opts.service, cluster_members['local'], output ):
        #   exit 0 if the node is running the service
        sys.exit(0)
    else:
        #   exit 1 if the node is NOT running the service
        sys.exit(1)


if __name__ == '__main__':
    main()