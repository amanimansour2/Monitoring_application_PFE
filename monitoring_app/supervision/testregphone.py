#!/usr/bin/python
from monitoring_app.models import Machine
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import json
from IPython import embed 
import sys
def get_regphone(id1):
    try:
        machine=Machine.objects.get(id=id1)
        print "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        s.sendline("python /home/amani/testscript/regestredphone.py")   # run a command
        s.prompt()             # match the prompt
        message=s.before  
        message=s.before  
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
       
        messages = json.loads(message)
        s.sendline ('exit')
        s.logout()
        return messages['phone']
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
