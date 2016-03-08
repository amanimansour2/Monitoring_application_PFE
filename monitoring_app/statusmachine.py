#!/usr/bin/python 
import pexpect
from monitoring_app.models import Machine
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import time
def get_statuss():
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        print "ccccc"
        s.sendline('python /home/amani/generalstatus.py' ) 
        s.prompt()
        message = s.before         
        s.logout()
        return message
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
