#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import subprocess
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys
import math
import os
from scapy.all import *
import os
import json
global res
def recpacket(scenarioinvite,interface,address ):
    dst_port="5060"
    print "sniffing on "+ interface + " filtre : src_addr = "+ address +"\n dst_port = "+ dst_port
    fltr="host "+address+" and udp and dst port "+dst_port
    test = True
    global va
    name="False"
    anonymous="False"
    SDP="False"
    va="FAIL"
    while test:
        p =sniff(iface=str(interface), filter=fltr , count=1 )	
        print "We received the following packet"
        p.show()
        print "###########"
        if(len(p)==0):
            va="FAIL"
            test=False
        else:
            L=[]
            if (scenarioinvite=="INVITE_with_name"):
                ch=p[0].sprintf("{Raw:%Raw.load%\n}")
                L=ch.split()
                if ("INVITE" in str(L[0])):
                    name="True"
                    test=False
            elif (scenarioinvite=="Anonymous_INVITE"):
                ch=p[0].sprintf("{Raw:%Raw.load%\n}")
                L=ch.split()
                if ("INVITE" in str(L[0])):
                    m=len(L)
                    for j in range(1,m):
                        if("sip:Anonymous@" in L[j]):
                            anonymous="True"
                            test=False
            elif (scenarioinvite=="INVITE_without_SDP"):
                ch=p[0].sprintf("{Raw:%Raw.load%\n}")
                L=ch.split()
                if ("INVITE" in str(L[0])):
                    m=len(L)
                    for j1 in range(1,m):
                        if("Content-Length" in L[j1]):
                            k=str(L[j1+1])
                            p1=k.find("\\")
                            if (int(k[:p1])==0):
                                SDP="True"
                                test=False
    if((anonymous=="True")and(scenarioinvite=="Anonymous_INVITE")):
       va="PASS ==> INVITE without name"
    elif((name=="True")and(scenarioinvite=="INVITE_with_name")):
       va="PASS ==>INVITE with name"
    elif((SDP=="True")and(scenarioinvite=="INVITE_without_SDP")):
       va="PASS ==>INVITE without SDP"
    else:
       va="FAIL"
    return va
def get_confcall(numsrc,numdest,scenarioinvite,id1,addphone,dure,interface,checked):
    try:
        machine=Machine.objects.get(id=id1)
        user=str(machine.username) 
        address=str(machine.address)
        password=str(machine.password)
        s = pxssh.pxssh()
        s.login (address,user, password)
        remotehost=password+"@"+address
        res="FAIL"
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
        if checked=="YES":
            os.popen(("tshark -i %s -a duration:%s -w /home/amani/projet/test.pcap &")%(interface,dure))
        s.sendline("python /home/%s/confcall.py  %s %s %s %s %s " % (user,adsrc,numsrc,numdest,scenarioinvite,addphone))   # run a command
        res=recpacket(scenarioinvite,interface,address)
        s.sendline("rm /home/%s/confcall.py  " % (user))
        os.system("exit")
        s.sendline ('exit')
        s.logout()
        return res      
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
