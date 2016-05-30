#!/usr/bin/python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys
import math
import os
from scapy.all import *

def snifff(interface, src_addr, nbre_pkt, dst_port, name_pcap):

    print "sniffing on "+ interface + " filtre : src_addr = "+ src_addr +"\n dest_port = "+ dst_port
    fltr="host "+src_addr+" and udp and dst port "+dst_port
    p = sniff(iface=str(interface), filter=fltr , count=nbre_pkt, timeout=20)
    c = wrpcap('/home/amani/'+name_pcap, p)
    s=len(p)
    L=[]
    name="False"
    anonymous="False"
    SDP="False"
    print "Number of packet received = " + str(s) + "\n \n"
    for i in range(0, s):
        ch=p[i].sprintf("{Raw:%Raw.load%\n}")
        L=ch.split()
        if ("INVITE" in str(L[0])):
            m=len(L)
            for j in range(1,m):
                if("sip:Anonymous@" in L[j]):
                    anonymous="True"
                    break
            for j1 in range(1,m):
                if("Content-Length" in L[j1]):
                    k=str(L[j1+1])
                    print str(k.find("\\"))
                    p1=k.find("\\")
                    print str(int(k[:p1]))
                    if (int(k[:p1])==0):
                        SDP="True"
                        break
            
            name="True"
            break
    if(anonymous=="True"):
       va="1"
    elif(SDP=="True"):
       va="2"
    elif(name=="True"):
       va="3"
    return va
	



