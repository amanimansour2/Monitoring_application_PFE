#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import time
import os
import json
def get_confcall1(numclient,addclient,scenarioreinvite,id1,dure,interface,checked):
    try:
        if checked=="YES":
            os.popen(("tshark -i %s -a duration:%s -w /home/amani/projet/test.pcap &")%(interface,dure))
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        remotehost=password+"@"+address
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uas.xml", remotehost, "/home/%s" %(user))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        machine1=Machine.objects.get(address=addclient)
        userc=str(machine1.username) 
        addressc=str(machine1.address)
        passwordc=str(machine1.password)
        sc = pxssh.pxssh()
        sc.login (addressc,userc, passwordc)
        remotehostc=passwordc+"@"+addressc
        COMMANDc="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uac.xml", remotehostc, "/home/%s" %(userc))
        childc = pexpect.spawn(COMMANDc)
        childc.expect(remotehostc+"'s password:")
        childc.sendline(passwordc)
        childc.expect(pexpect.EOF)
        s.sendline('cd /usr/src/sipp.svn')

        s.sendline('./sipp -sf /home/%s/uas.xml -i %s -m 1 '% (user,address))
        sc.sendline('cd /usr/src/sipp.svn')
        sc.sendline('./sipp -sf /home/%s/uac.xml   -i %s:%s -s %s %s:%s -m 1'% (userc,addclient,"5060",numclient,address,"5060")) 
        s.prompt()
        m=s.before
        print  m
        time.sleep(6)
        return "done"      
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
