#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import json
def get_confcall(numsrc,numdest,scenarioinvite,id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        remotehost=password+"@"+address
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/confcall.py", remotehost, "/home/%s" %(user))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        machines =  Machine.objects.all()
        for machine in machines:
            if int(machine.id) == int(id1) :
                adsrc=machine.address
        s.sendline('su -')
        s.sendline(password)
        s.sendline("python /home/%s/confcall.py  %s %s %s %s " % (user,adsrc,numsrc,numdest,scenarioinvite))   # run a command
        s.prompt()             # match the prompt
        message=s.before 
        print message
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        
        messages = json.loads(message)
        s.sendline ('exit')
        s.logout()
        return messages['statnumber']      
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
