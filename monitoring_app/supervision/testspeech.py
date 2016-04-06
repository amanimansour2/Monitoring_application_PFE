import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import os
import sys
import subprocess as sub
import json
import time
import subprocess
from monitoring_app.models import Machine
import time
def get_begincall(namepcap,id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        remotehost=password+"@"+address
        COMMAND="scp  -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/recup_client_call.py", remotehost, "/home/%s" %(user))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        s.sendline('su -')
        s.sendline(password)
        s.sendline('cd /home/%s' %(user))
        s.sendline('python /home/%s/recup_client_call.py %s ' %(user,namepcap))   # run a command
        time.sleep(20)
        s.sendline('chmod +777 /home/%s/%s ' %(user,namepcap))   # run a command   
        COMMAND="scp  -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/%s", remotehost, "/home/%s" %(user))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        s.prompt()  
        		# match the prompt
        os.chdir("/home/amani/projet/PFE/monitoring_app/scripttest/")
        p = sub.Popen(('python', '/home/amani/projet/PFE/monitoring_app/scripttest/speech.py','/home/%s/%s' %(user,namepcap)),stdout=sub.PIPE) 
        message=p.stdout.read()
        print message
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        
        messages = json.loads(message)
        s.sendline ('exit')
        s.logout()
        return messages['wavname']   
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0

