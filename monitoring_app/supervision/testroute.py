#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine

import getpass
import sys
def get_route(id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        s.sendline("python /home/amani/testscript/defaultrout.py")   # run a command
        s.prompt()             # match the prompt
        message=s.before          # print everything before the prompt.
        s.sendline ('exit')
        s.logout()
        return message
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0

