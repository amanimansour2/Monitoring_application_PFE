#!/usr/bin/python
from lxml import etree
import xml.etree.ElementTree
import lxml.etree
from StringIO import StringIO
import os
import ESL
import pexpect
import subprocess
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import json
from lxml.builder import E
import sys 
import time
import json
import ast
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
d={}


adsrc=sys.argv[1]
numsrc=sys.argv[2]
numdest=sys.argv[3]
scenarioinvite=sys.argv[4]
addphone=sys.argv[5]
if scenarioinvite=="INVITE_with_name":
    con.api("originate", "sofia/gateway/gateway_to_%s.xml/%s &park()" %(numsrc,numdest))
elif scenarioinvite=="Anonymous_INVITE":
    tree = etree.parse("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml")
    for extension in tree.xpath("/include/user/variables/variable"):
        if str(extension.get('name'))=="effective_caller_id_name":
            c=extension.get('value')  
            c1=c            
            f = open("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml", 'w')
            r=c.replace(c,"Anonymous")
            extension.set('value',r)
            print extension.get('value')
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
        elif str(extension.get('name'))=="effective_caller_id_number":
            c=extension.get('value') 
            c2=c			
            f = open("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml", 'w')
            r=c.replace(c,"Anonymous")
            extension.set('value',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    ch=''
    for context in tree.xpath("/include/context"): 
        for extension in tree.xpath("/include/context/extension"):                           
            ch+=str(extension.get('name'))
        if ("Anonymous INVITE to"+numdest in ch)==False:
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            y=etree.XML('<extension />')
            y.set('name',"Anonymous INVITE to "+numdest+" from "+numsrc)
            context.insert(1,y)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()
            if con.connected():
                con.api("reloadxml")
            for extension in tree.xpath("/include/context/extension"):              
                ext=extension.get('name')
                if str(ext)=="Anonymous INVITE to "+numdest+" from "+numsrc :
                    f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                    y=etree.XML('<condition field="destination_number"/>')
                    y.set('expression',"^("+numdest+")$")
                    l1=etree.XML('<action application="export"/>')
                    l1.set('data',"dialed_extension=$1")
                    y.append(l1)
                    l6=etree.XML('<action application="privacy"/>')
                    l6.set('data',"full")
                    y.append(l6)
                    l8=etree.XML('<action application="set"/>')
                    l8.set('data',"caller_id_number="+numsrc)
                    y.append(l8)
                    l81=etree.XML('<action application="set"/>')
                    l81.set('data',"caller_id_name=Anonymous")
                    y.append(l81)
                    l84=etree.XML('<action application="set"/>')
                    l84.set('data',"sip_h_P-Asserted-Identity=\"${caller_id_number}\"<sip:${caller_id_number}@"+adsrc+">")
                    y.append(l84)
                    l81=etree.XML('<action application="set"/>')
                    l81.set('data',"sip_h_Privacy=id")
                    y.append(l81)
                    l10=etree.XML('<action application="bridge"/>')
                    l10.set('data',"user/${dialed_extension}@${domain_name}")
                    y.append(l10)
                    extension.append(y)
                    f.write(etree.tostring(tree, pretty_print=True))
                    f.close()
                    con.api("reloadxml")
    con.api("originate", "sofia/gateway/gateway_to_%s.xml/%s &park()" %(numsrc,numdest)) 
elif scenarioinvite=="INVITE_without_SDP":
    con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
    con.api('sofia','profile external restart')
    time.sleep(2)
    e = con.api("sofia status profile internal reg")
    ch=e.getBody()
    ch1=ch
    j,p,k,l=0,0,0,0
    testnum=":"+numdest+"@"
    while j<1:
        k=ch1.find("Contact:")
        p=p+k+len("Contact:")+3
        ch1=ch[p:]
        l=ch1.find("\n")
        if testnum in ch1[:l]:
            j=j+1
            contact=ch1[:l]
    z,t=0,0
    z=contact.find(":")
    contact=contact[z+1:]
    z=contact.find(":")
    t=contact.find("@")
    add=contact[t+1:z]
    contact=contact[z+1:]
    z=contact.find(">")
    portdest=contact[:z]
    val=numsrc
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    PROTOCOLE="u1"
    CALL="1"
    RATE="1000"
    ENDCALL="1"
    DURATION="800"
    SIPP2_PORT=portdest
    SERVICE_NAME=numdest
    SIPP2_IP=add
    os.chdir('/usr/src/sipp.svn')
    ipcmd = 'iptables -t nat -A POSTROUTING -p udp --sport '+SIPP1_PORT+' -j SNAT --to 192.168.3.5:5060'
    os.system(ipcmd)
    ch1="<?xml version=\"1.0\" encoding="+"\"ISO-8859-1\""+" ?>\n<scenario name="+"\"invite without SDP\""+">\n  <send >\n    <![CDATA[\n      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip];branch=z9hG4bK1ref2n30e800fb4nu741.1\n      Session-Expires: 1800\n      From:<sip:%s@[local_ip] >;tag=[call_number]\n      To: <sip:[service]@[remote_ip]:[remote_port]>\n      Call-ID: [call_id]\n      CSeq: 1 INVITE\n      Contact: <sip:sipp@[local_ip]:5060;transport=udp>\n      Max-Forwards: 70\n      Allow: ACK,BYE,CANCEL,INVITE,NOTIFY,REFER,UPDATE,OPTIONS,SUBSCRIBE,INFO\n      Accept: application/sdp\n      Supported: timer,replaces\n      P-Asserted-Identity: <sip:$val@[local_ip]>\n      Privacy: none\n      User-Agent: SIPp\n      Content-Length: 0\n    ]]>\n  </send> \n </scenario>" %(val)
    ch2="#!"+"/usr/bin/python \nimport os \nval=\"%s\"\nSIPP1_IP=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP1_PORT=\"%s\"\nPROTOCOLE=\"%s\"\nCALL=\"%s\"\nRATE=\"%s\"\nENDCALL=\"%s\"\nDURATION=\"%s\"\nSIPP2_PORT=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP2_IP=\"%s\"\nprint \"Lancement du client SIPp ...\" \nos.system('./sipp -t '+PROTOCOLE+' -r '+CALL+' -s  '+SERVICE_NAME+' -m '+ENDCALL+' -i '+ SIPP1_IP+' -p '+SIPP1_PORT+' -sf  invite_sans_SDP1.xml -d '+DURATION+' -nr -max_retrans 1 '+SIPP2_IP+':'+SIPP2_PORT)\nprint \"Appels termines.\"" %(val,SIPP1_IP,SERVICE_NAME,SIPP1_PORT,PROTOCOLE,CALL,RATE,ENDCALL,DURATION,SIPP2_PORT,SERVICE_NAME,SIPP2_IP)
    if not os.path.exists('invite_sans_SDP1.xml'): 
        f=open('invite_sans_SDP1.xml', 'w')
        f.write(ch1)
        f.close()
    if not os.path.exists('invite_sans_SDP1'): 
        f=open('invite_sans_SDP1', 'w')
        f.write(ch2)
        f.close()
    os.system("python invite_sans_SDP1")
    if os.path.exists('invite_sans_SDP1'): 
        os.remove('invite_sans_SDP1')
    if os.path.exists('invite_sans_SDP1.xml'): 
        os.remove('invite_sans_SDP1.xml')
    ipcmd = 'iptables -t nat -D POSTROUTING -p udp --sport '+SIPP1_PORT+' -j SNAT --to 192.168.3.5:5060'
    os.system(ipcmd)
elif scenarioinvite=="DTMF":
    con.api("originate", "{origination_caller_id_number=1700,origination_caller_id_name=1700}user/1500 sofia/external/1700@192.168.3.5")
elif scenarioinvite=="Service_Unavailable":
    val=numsrc
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    PROTOCOLE="u1"
    CALL="1"
    RATE="1000"
    ENDCALL="1"
    DURATION="800"
    SIPP2_PORT="5061"
    SERVICE_NAME=numdest
    SIPP2_IP=addphone
    os.chdir('/usr/src/sipp.svn')
    ch2="#!"+"/usr/bin/python \nimport os \nval=\"%s\"\nSIPP1_IP=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP1_PORT=\"%s\"\nPROTOCOLE=\"%s\"\nCALL=\"%s\"\nRATE=\"%s\"\nENDCALL=\"%s\"\nDURATION=\"%s\"\nSIPP2_PORT=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP2_IP=\"%s\"\nprint \"Lancement du client SIPp ...\" \nos.system('./sipp -t '+PROTOCOLE+' -r '+CALL+' -s  '+SERVICE_NAME+' -m '+ENDCALL+' -i '+ SIPP1_IP+' -p '+SIPP1_PORT+' -sf  uac.xml -d '+DURATION+' -nr -max_retrans 1 '+SIPP2_IP+':'+SIPP2_PORT)\nprint \"Appels termines.\"" %(val,SIPP1_IP,SERVICE_NAME,SIPP1_PORT,PROTOCOLE,CALL,RATE,ENDCALL,DURATION,SIPP2_PORT,SERVICE_NAME,SIPP2_IP)
    ch1="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<!DOCTYPE scenario SYSTEM \"sipp.dtd\">\n \n<scenario name=\"UAC\">\n  <send >\n   <![CDATA[\n       INVITE sip:[service]@[remote_ip] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=z9hG4bK1ref2n30e800fb4nu741\n      From: <sip:%s@[local_ip]>;tag=[call_number]\n      To: <sip:[service]@[remote_ip]:[remote_port]>\n      Call-ID: [call_id]\n  CSeq: 1 INVITE\n      Contact: <sip:%s@[local_ip]:[local_port];transport=udp>\n      Max-Forwards: 70\n      Allow: ACK,BYE,CANCEL,INVITE,NOTIFY,REFER,UPDATE,OPTIONS,SUBSCRIBE,INFO\n      Accept: application/sdp\n      Privacy: none\n      User-Agent: SIPp\n      Content-Type: application/sdp\n      Content-Length: 0\n  ]]>\n  </send>\n   <recv response=\"100\" optional=\"true\">\n  </recv>\n  <recv response=\"180\" optional=\"true\">\n  </recv>\n  <recv response=\"200\">\n  </recv>\n  <send >\n    <![CDATA[\n      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\nFrom:<sip:%s@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\nTo:<sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\nCall-ID: [call_id]\nCSeq: 2 INVITE\nContact: sip:%s@[local_ip]:[local_port]\nMax-Forwards: 70\nContent-Length: 0\n]]>\n</send>\n<recv response=\"503\">\n</recv>\n</scenario>"%(val,val,val,val)
    if not os.path.exists('uac.xml'): 
        f=open('uac.xml', 'w')
        f.write(ch1)
        f.close()
    if not os.path.exists('test503'): 
        f=open('test503', 'w')
        f.write(ch2)
        f.close()
    os.system("python test503")
    if os.path.exists('test503'): 
        os.remove('test491')
    if os.path.exists('uac.xml'): 
        os.remove('uac.xml')
elif scenarioinvite=="Busy_Everywhere":
    val=numsrc
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    PROTOCOLE="u1"
    CALL="1"
    RATE="1000"
    ENDCALL="1"
    DURATION="800"
    SIPP2_PORT="5061"
    SERVICE_NAME=numdest
    SIPP2_IP=addphone
    os.chdir('/usr/src/sipp.svn')
    ch2="#!"+"/usr/bin/python \nimport os \nval=\"%s\"\nSIPP1_IP=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP1_PORT=\"%s\"\nPROTOCOLE=\"%s\"\nCALL=\"%s\"\nRATE=\"%s\"\nENDCALL=\"%s\"\nDURATION=\"%s\"\nSIPP2_PORT=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP2_IP=\"%s\"\nprint \"Lancement du client SIPp ...\" \nos.system('./sipp -t '+PROTOCOLE+' -r '+CALL+' -s  '+SERVICE_NAME+' -m '+ENDCALL+' -i '+ SIPP1_IP+' -p '+SIPP1_PORT+' -sf  uac.xml -d '+DURATION+' -nr -max_retrans 1 '+SIPP2_IP+':'+SIPP2_PORT)\nprint \"Appels termines.\"" %(val,SIPP1_IP,SERVICE_NAME,SIPP1_PORT,PROTOCOLE,CALL,RATE,ENDCALL,DURATION,SIPP2_PORT,SERVICE_NAME,SIPP2_IP)
    ch1="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<!DOCTYPE scenario SYSTEM \"sipp.dtd\">\n \n<scenario name=\"UAC\">\n  <send >\n   <![CDATA[\n       INVITE sip:[service]@[remote_ip] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=z9hG4bK1ref2n30e800fb4nu741\n      From: <sip:%s@[local_ip]>;tag=[call_number]\n      To: <sip:[service]@[remote_ip]:[remote_port]>\n      Call-ID: [call_id]\n  CSeq: 1 INVITE\n      Contact: <sip:%s@[local_ip]:[local_port];transport=udp>\n      Max-Forwards: 70\n      Allow: ACK,BYE,CANCEL,INVITE,NOTIFY,REFER,UPDATE,OPTIONS,SUBSCRIBE,INFO\n      Accept: application/sdp\n      Privacy: none\n      User-Agent: SIPp\n      Content-Type: application/sdp\n      Content-Length: 0\n  ]]>\n  </send>\n   <recv response=\"100\" optional=\"true\">\n  </recv>\n  <recv response=\"180\" optional=\"true\">\n  </recv>\n  <recv response=\"200\">\n  </recv>\n  <send >\n    <![CDATA[\n      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\nFrom:<sip:%s@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\nTo:<sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\nCall-ID: [call_id]\nCSeq: 2 INVITE\nContact: sip:%s@[local_ip]:[local_port]\nMax-Forwards: 70\nContent-Length: 0\n]]>\n</send>\n<recv response=\"600\">\n</recv>\n</scenario>"%(val,val,val,val)
    if not os.path.exists('uac.xml'): 
        f=open('uac.xml', 'w')
        f.write(ch1)
        f.close()
    if not os.path.exists('test600'): 
        f=open('test600', 'w')
        f.write(ch2)
        f.close()
    os.system("python test600")
    if os.path.exists('test600'): 
        os.remove('test600')
    if os.path.exists('uac.xml'): 
        os.remove('uac.xml')
elif scenarioinvite=="Temporarily_Unavailable":
    val=numsrc
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    PROTOCOLE="u1"
    CALL="1"
    RATE="1000"
    ENDCALL="1"
    DURATION="800"
    SIPP2_PORT="5061"
    SERVICE_NAME=numdest
    SIPP2_IP=addphone
    os.chdir('/usr/src/sipp.svn')
    ch2="#!"+"/usr/bin/python \nimport os \nval=\"%s\"\nSIPP1_IP=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP1_PORT=\"%s\"\nPROTOCOLE=\"%s\"\nCALL=\"%s\"\nRATE=\"%s\"\nENDCALL=\"%s\"\nDURATION=\"%s\"\nSIPP2_PORT=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP2_IP=\"%s\"\nprint \"Lancement du client SIPp ...\" \nos.system('./sipp -t '+PROTOCOLE+' -r '+CALL+' -s  '+SERVICE_NAME+' -m '+ENDCALL+' -i '+ SIPP1_IP+' -p '+SIPP1_PORT+' -sf  uac.xml -d '+DURATION+' -nr -max_retrans 1 '+SIPP2_IP+':'+SIPP2_PORT)\nprint \"Appels termines.\"" %(val,SIPP1_IP,SERVICE_NAME,SIPP1_PORT,PROTOCOLE,CALL,RATE,ENDCALL,DURATION,SIPP2_PORT,SERVICE_NAME,SIPP2_IP)
    ch1="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<!DOCTYPE scenario SYSTEM \"sipp.dtd\">\n \n<scenario name=\"UAC\">\n  <send >\n   <![CDATA[\n       INVITE sip:[service]@[remote_ip] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=z9hG4bK1ref2n30e800fb4nu741\n      From: <sip:%s@[local_ip]>;tag=[call_number]\n      To: <sip:[service]@[remote_ip]:[remote_port]>\n      Call-ID: [call_id]\n  CSeq: 1 INVITE\n      Contact: <sip:%s@[local_ip]:[local_port];transport=udp>\n      Max-Forwards: 70\n      Allow: ACK,BYE,CANCEL,INVITE,NOTIFY,REFER,UPDATE,OPTIONS,SUBSCRIBE,INFO\n      Accept: application/sdp\n      Privacy: none\n      User-Agent: SIPp\n      Content-Type: application/sdp\n      Content-Length: 0\n  ]]>\n  </send>\n   <recv response=\"100\" optional=\"true\">\n  </recv>\n  <recv response=\"180\" optional=\"true\">\n  </recv>\n  <recv response=\"200\">\n  </recv>\n  <send >\n    <![CDATA[\n      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\nFrom:<sip:%s@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\nTo:<sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\nCall-ID: [call_id]\nCSeq: 2 INVITE\nContact: sip:%s@[local_ip]:[local_port]\nMax-Forwards: 70\nContent-Length: 0\n]]>\n</send>\n<recv response=\"480\">\n</recv>\n</scenario>"%(val,val,val,val)
    if not os.path.exists('uac.xml'): 
        f=open('uac.xml', 'w')
        f.write(ch1)
        f.close()
    if not os.path.exists('test480'): 
        f=open('test480', 'w')
        f.write(ch2)
        f.close()
    os.system("python test480")
    if os.path.exists('test480'): 
        os.remove('test480')
    if os.path.exists('uac.xml'): 
        os.remove('uac.xml')
elif scenarioinvite=="Pending_Request":
    val=numsrc
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    PROTOCOLE="u1"
    CALL="1"
    RATE="1000"
    ENDCALL="1"
    DURATION="800"
    SIPP2_PORT="5061"
    SERVICE_NAME=numdest
    SIPP2_IP=addphone
    os.chdir('/usr/src/sipp.svn')
    ch2="#!"+"/usr/bin/python \nimport os \nval=\"%s\"\nSIPP1_IP=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP1_PORT=\"%s\"\nPROTOCOLE=\"%s\"\nCALL=\"%s\"\nRATE=\"%s\"\nENDCALL=\"%s\"\nDURATION=\"%s\"\nSIPP2_PORT=\"%s\"\nSERVICE_NAME=\"%s\"\nSIPP2_IP=\"%s\"\nprint \"Lancement du client SIPp ...\" \nos.system('./sipp -t '+PROTOCOLE+' -r '+CALL+' -s  '+SERVICE_NAME+' -m '+ENDCALL+' -i '+ SIPP1_IP+' -p '+SIPP1_PORT+' -sf  uac.xml -d '+DURATION+' -nr -max_retrans 1 '+SIPP2_IP+':'+SIPP2_PORT)\nprint \"Appels termines.\"" %(val,SIPP1_IP,SERVICE_NAME,SIPP1_PORT,PROTOCOLE,CALL,RATE,ENDCALL,DURATION,SIPP2_PORT,SERVICE_NAME,SIPP2_IP)
    ch1="<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<!DOCTYPE scenario SYSTEM \"sipp.dtd\">\n \n<scenario name=\"UAC\">\n  <send >\n   <![CDATA[\n       INVITE sip:[service]@[remote_ip] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=z9hG4bK1ref2n30e800fb4nu741\n      From: <sip:%s@[local_ip]>;tag=[call_number]\n      To: <sip:[service]@[remote_ip]:[remote_port]>\n      Call-ID: [call_id]\n  CSeq: 1 INVITE\n      Contact: <sip:%s@[local_ip]:[local_port];transport=udp>\n      Max-Forwards: 70\n      Allow: ACK,BYE,CANCEL,INVITE,NOTIFY,REFER,UPDATE,OPTIONS,SUBSCRIBE,INFO\n      Accept: application/sdp\n      Privacy: none\n      User-Agent: SIPp\n      Content-Type: application/sdp\n      Content-Length: 0\n  ]]>\n  </send>\n   <recv response=\"100\" optional=\"true\">\n  </recv>\n  <recv response=\"180\" optional=\"true\">\n  </recv>\n  <recv response=\"200\">\n  </recv>\n  <send >\n    <![CDATA[\n      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\n      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\nFrom:<sip:%s@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\nTo:<sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\nCall-ID: [call_id]\nCSeq: 2 INVITE\nContact: sip:%s@[local_ip]:[local_port]\nMax-Forwards: 70\nContent-Length: 0\n]]>\n</send>\n<recv response=\"491\">\n</recv>\n</scenario>"%(val,val,val,val)
    if not os.path.exists('uac.xml'): 
        f=open('uac.xml', 'w')
        f.write(ch1)
        f.close()
    if not os.path.exists('test491'): 
        f=open('test491', 'w')
        f.write(ch2)
        f.close()
    os.system("python test491")
    if os.path.exists('test491'): 
        os.remove('test491')
    if os.path.exists('uac.xml'): 
        os.remove('uac.xml')
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
time.sleep(1)
state=True
if state==True:
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for context in tree.xpath("/include/context"): 
        for extension in tree.xpath("/include/context/extension"):                           
            if (extension.get('name')=="Anonymous INVITE to "+numdest+" from "+numsrc ):
                extension.getparent().remove(extension)
                f= open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml")
    for extension in tree.xpath("/include/user/variables/variable"):
        if str(extension.get('name'))=="effective_caller_id_name":
            c=extension.get('value')              
            f = open("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml", 'w')
            r=c.replace(c,"Extension "+numsrc)
            extension.set('value',r)
            print extension.get('value')
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
        elif str(extension.get('name'))=="effective_caller_id_number":
            c=extension.get('value') 
            c2=c			
            f = open("/usr/local/freeswitch/conf/directory/default/"+numsrc+".xml", 'w')
            r=c.replace(c,numsrc)
            extension.set('value',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")				

if con.connected():
    con.api("reloadxml")
time.sleep(1)
d["statnumber"]= "done"

print d


