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
def get_begincall(time1,id1):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        os.popen(("tcpdump -i %s -n 'udp and src host 192.168.3.1' -w /home/%s &")%("enp0s8","speech.pcap")) 
        time.sleep(time1)
        os.chdir("/home/amani/projet/PFE/monitoring_app/scripttest/")
        p = sub.Popen(('python', '/home/amani/projet/PFE/monitoring_app/scripttest/speech.py','/home/%s' %("speech.pcap")),stdout=sub.PIPE) 
        message=p.stdout.read()
        i=message.find('{')
        j=message.find('}')+1
        message=message[i:j]
        message= message.replace("'", "\"")
        return message['wavname']   
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0

