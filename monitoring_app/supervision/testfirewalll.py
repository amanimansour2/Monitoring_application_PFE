#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import iptc
from IPython import embed
import json
def get_firewall(id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.sendline('su -')
        s.sendline('amani')
        s.login (address,user, password) 
        s.sendline("python /home/amani/testscript/firewall_test.py")   # run a command
        s.prompt()             # match the prompt
        message=s.before  
        print message 
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        messages = json.loads(message)
        s.logout()
        return messages['firewall']
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
