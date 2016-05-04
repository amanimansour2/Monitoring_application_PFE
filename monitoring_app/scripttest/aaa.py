#!/usr/bin/python
# -*- coding: ascii -*-
# coding: latin-1
from lxml import etree
import xml.etree.ElementTree
import lxml.etree
from StringIO import StringIO
import os
import ESL
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import json
from lxml.builder import E
import sys 
import time
import json
import ast

d={}
adsrc="192.168.3.5"
number="1"
SIPP1_IP="192.168.3.5"
SIPP1_PORT="5061"
SIPP2_PORT="192.168.3.1"
os.chdir('/usr/src/sipp.svn') 
ch1="#!/usr/bin/python/ \nimport os \nimport time \nos.system(\"iptables -t nat -A POSTROUTING  -p udp --sport %s -j SNAT --to  %s:5060\") \nos.system(\" iptables -t nat -A PREROUTING  -p udp -s %s -j DNAT --to-destination  %s:%s \") \nos.system(\"iptables -t nat -L\") \nos.system(\"./sipp -sf testregister.xml -m %s\")\nos.system(\" iptables -F \") \nos.system(\"iptables -X \") \nos.system(\" iptables -t nat -F \") \nos.system(\" iptables -t nat -X \") \nos.system(\" iptables -t mangle -F \")\nos.system(\" iptables -t mangle -X \") \nos.system(\"iptables -P INPUT ACCEPT \") \nos.system(\" iptables -P OUTPUT ACCEPT \") \nos.system(\"iptables -P FORWARD ACCEPT \") \nos.system(\"iptables -t nat -L\")" %(SIPP1_PORT,SIPP1_IP,SIPP2_PORT,SIPP1_IP,SIPP1_PORT,number)
ch2="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<!DOCTYPE scenario SYSTEM \"sipp.dtd\">\n\n<scenario name=\"Basic UAS responder\">\n<recv request=\"REGISTER\" crlf=\"true\">\n  </recv>\n  <send>\n    <![CDATA[ \n      SIP/2.0 401 Unauthorized \n      [last_Via:]\n      [last_From:]\n      [last_To:];tag=[pid]SIPpTag01[call_number]\n      [last_Call-ID:]\n      [last_CSeq:]\n      Contact: <sip:[local_ip]:[local_port];transport=[transport]>\n      WWW-Authenticate: Digest realm=\"%s\", nonce=\"47ebe028cda119c35d4877b383027d28da013815\"\n      Content-Length: 0\n    ]]>\n  </send>\n  <recv request=\"REGISTER\" crlf=\"true\">\n  </recv>\n  <send>\n    <![CDATA[\n      SIP/2.0 401 Unauthorized\n      [last_Via:]\n      [last_From:]\n      [last_To:];tag=[pid]SIPpTag01[call_number]\n      [last_Call-ID:]\n      [last_CSeq:]\n      Contact: <sip:[local_ip]:[local_port];transport=[transport]>\n      WWW-Authenticate: Digest realm=\"%s\",Stale = False, nonce=\"47ebe028cda3284789cda42390815234bcedf\"\n      Content-Length: 0\n    ]]>\n  </send>\n</scenario>" %(adsrc,adsrc)
if not os.path.exists('testregister.xml'): 
    f=open('testregister.xml', 'w')
    f.write(ch2)
    f.close()
if not os.path.exists('register.py'): 
    f=open('register.py', 'w')
    f.write(ch1)
    f.close()
	
os.system("python register.py")
if os.path.exists('register.py'): 
    os.remove('register.py')
if os.path.exists('testregister.xml'): 
    os.remove('testregister.xml')
d["statnumber"]= "done"

print d


