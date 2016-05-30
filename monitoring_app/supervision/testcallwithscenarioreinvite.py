#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
from monitoring_app.models import Machine
import getpass
import sys
import time
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys
import math
import os
from scapy.all import *
import json
global res
def recpacket(numclient,addclient,numscenario,interface):
    test = True
    global va
    va="FAIL"
    err=False
    ref=["INVITE","100","180","200","ACK","INVITE",numscenario]
    while test:
        p =sniff(iface=str(interface), filter="udp" , timeout=15)	
        print "We received the following packet"
        p.show()
        m=[]
        s=len(p)
        j,r,r1=0,0,0
        L=[]
        for i in range(0, s):
            m.append(p[i])
        if((s==0)or (s<7)):
            va="FAIL"
            test=False
        else:
            while j<s:
                ch=p[j].sprintf("{Raw:%Raw.load%\n}")
                oo=ch.split()
                print type(len(oo))
                print str(len(oo))
                if(len(oo)>=2) :
                    L+=[[ch.split()[0],ch.split()[1]]]
                    j=j+1
                else:
                    j=j+1
            for k in range(0,7):
                if len(L)==7:
                    if (ref[k] in L[k][0]) or(ref[k] in L[k][1]):
                        pass 
                    else:
                        va="FAIL"
                        test=False
                    va="PASS"
                else:
                    for n in range(r,len(L)):
                        if (ref[k] in L[n][0]) or(ref[k] in L[n][1]):
                            r=k+1+r1
                            va="PASS"
                            break
                        elif (ref[k] not in L[n][0])and(ref[k] not in L[n][1]):
                            r1=r1+1
                            va="FAIL"
                  
					
        print va			
        return va
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
        if scenarioreinvite=="Pending_Request":
		    numscenario="491"
        elif scenarioreinvite=="Temporarily_Unavailable":
		    numscenario="480"
        elif scenarioreinvite=="Busy_Everywhere":
		    numscenario="600"
        elif scenarioreinvite=="Service_Unavailable":
		    numscenario="503"
        COMMAND="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uas%s.xml"%(numscenario), remotehost, "/home/%s" %(user))
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
        COMMANDc="scp -oPubKeyAuthentication=no %s %s:%s " % ("/home/amani/projet/PFE/monitoring_app/scripttest/uac%s.xml"%(numscenario), remotehostc, "/home/%s" %(userc))
        childc = pexpect.spawn(COMMANDc)
        childc.expect(remotehostc+"'s password:")
        childc.sendline(passwordc)
        childc.expect(pexpect.EOF)
        s.sendline('cd /usr/src/sipp.svn')

        s.sendline('./sipp -sf /home/%s/uas%s.xml -i %s -m 1 '% (user,numscenario,address))
        sc.sendline('cd /usr/src/sipp.svn')
        sc.sendline('./sipp -sf /home/%s/uac%s.xml   -i %s -s %s %s:%s -m 1'% (userc,numscenario,addclient,numclient,address,"5061")) 
        res=recpacket(numclient,addclient,numscenario,interface)
        s.prompt()
        m=s.before
        return res      
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0
