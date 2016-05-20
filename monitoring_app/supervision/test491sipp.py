#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import time
import os
import json
def get_sipp491(id1,id2):
    try:
        machineserver=Machine.objects.get(id=id2)
        users=str(machineserver.username) 
        addresss=str(machineserver.address)
        passwords=str(machineserver.password)
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        remotehosts=passwords+"@"+addresss
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uas.xml", remotehosts, "/home/%s" %(users))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehosts+"'s password:")
        child.sendline(passwords)
        child.expect(pexpect.EOF)
        remotehost=password+"@"+address
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uac.xml", remotehost, "/home/%s" %(user))
        child = pexpect.spawn(COMMAND)
        child.expect(remotehost+"'s password:")
        child.sendline(password)
        child.expect(pexpect.EOF)
        os.chdir("/usr/src/sipp.svn/")
        machines =  Machine.objects.all()
        s.login (address,user, password)
        os.system(("cp /home/%s/uas.xml /usr/src/sipp.svn/uas.xml")%(users))
        os.system(("./sipp -sf uas.xml -i %s -s 1500 -m 1 &")%(addresss))
        s.sendline('su -')
        s.sendline(password)
        s.sendline(("cp /home/%s/uac.xml /usr/src/sipp.svn/uac.xml")%(user))
        s.sendline("cd /usr/src/sipp.svn/")
        s.sendline("./sipp -sf uac.xml -m 1 -i %s:%s -s 1500 %s:%s" % (address,"5060",addresss,"5061"))   # run a command
        os.system("rm /usr/src/sipp.svn/uas.xml")
        time.sleep(1)
        s.sendline("rm /usr/src/sipp.svn/%s" %("uac.xml"))
        s.sendline ('exit')
        s.logout()
        return "done"      
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
