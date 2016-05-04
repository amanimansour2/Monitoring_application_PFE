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
        s.login (address,user, password)
        remotehost=password+"@"+address
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/firewall_test.py", remotehost, "/home/%s" %(user) )
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        s.sendline('su -')
        s.sendline(password)
        s.sendline('cd /home/%s/' % (user))
        s.sendline("python  /home/%s/firewall_test.py"  % (user) )   # run a command
        s.prompt()             # match the prompt
        message=s.before  
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        messages = json.loads(message)
        s.sendline("rm  /home/%s/firewall_test.py"  % (user) )   # run a command
        s.sendline ('exit')
        s.logout()
        return messages['firewall']
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
