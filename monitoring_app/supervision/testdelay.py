import pexpect
from monitoring_app.models import Machine
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import time
import json 

def get_delay(id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        s.sendline('python /home/amani/testscript/delay.py ' )   # run a command
        s.prompt()
        message = s.before          # print everything before the prompt.
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        messages = json.loads(message)
        s.logout()
        return messages['delay']
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0


