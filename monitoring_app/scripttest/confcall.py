#!/usr/bin/python
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
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
d={}

adsrc=sys.argv[1]
numsrc=sys.argv[2]
numdest=sys.argv[3]
scenarioinvite=sys.argv[4]
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
    con.api("originate", "{origination_caller_id_number=1700,origination_caller_id_name=1700}user/1500 sofia/external/1700@192.168.3.5")
elif scenarioinvite=="Send_DTMF":
    con.api("originate", "{origination_caller_id_number=1700,origination_caller_id_name=1700}user/1500 sofia/external/1700@192.168.3.5")
con.api("exit")
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
                print "oui"
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


