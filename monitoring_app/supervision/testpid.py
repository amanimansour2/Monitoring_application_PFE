import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
from monitoring_app.models import Machine
import time
def get_pid(process_name,id1):
    try:
       
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        s.sendline('python /home/amani/testscript/pid.py ' + process_name )   # run a command
        s.prompt()             # match the prompt
        message = s.before          # print everything before the prompt.
        s.logout()
        return message
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0

