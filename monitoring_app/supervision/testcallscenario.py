#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import os
import time
import json
def get_testcall(id1,dure,interface,checked):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)

        if checked=="YES":
            os.popen(("tshark -i %s -a duration:%s -w /home/amani/projet/test.pcap &")%(interface,dure))
        os.system("exit")
        return "done"     
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
