#!/usr/bin/python 
import pexpect
from monitoring_app.models import Machine
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import time
import json
from testdelay import get_delay
from testdisk import get_disk
from testroute import get_route
from testvolfile import get_volfile
from testfirewall import get_firewall
from testcpu import get_cpu
from IPython import embed
from testservices import get_services

def get_statuss(id1):
    try:
        if get_delay(id1)=="True":
		    return "rouge !!!"
        elif get_disk(id1)=="Risk":
		    return "orange !!!"
        elif get_route(id1)=="False" :
		    return "rouge !!! "
        elif get_volfile(id1)=="True":
		    return "orange !!!"
        elif get_firewall(id1)=="True":
		    return "rouge !!!"
        elif (str(get_services(id1)[2])== 'OFF' )or(str(get_services(id1)[3])== 'OFF')or(str(get_services(id1)[0])== 'OFF')or str(get_services(id1)[1])== 'OFF':
            return "orange !!!"
        elif get_firewall(id1)=="True":
		    return "orange !!!"
        else:
		    return "Vert !!!"
		    
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
