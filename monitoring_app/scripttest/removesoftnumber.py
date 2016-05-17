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
import json
import ast

d={}
ch=sys.argv[1]
point=ch.find("=")
adsrc=ch[:point]
numero=ch[point+1:len(ch)]
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
os.remove("/usr/local/freeswitch/conf/directory/default/"+numero+".xml")
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
for extension in tree.xpath("/include/context/extension"):
    if str(extension.get('name'))=="Local_Extension":
        c=extension.find('condition').get('expression')            
        if numero in c :  
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c.replace("|"+str(numero),"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
    if str(extension.get('name'))=="DTMF_FOR_"+numero:
        extension.getparent().remove(extension)        
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        con.api("reloadxml")
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/public.xml")
for extension in tree.xpath("/include/context/extension"):
    if str(extension.get('name'))=="public_extensions":
        c=extension.find('condition').get('expression')            
        if numero in c :  
            f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
            r=c.replace("|"+str(numero),"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
for extension in tree.xpath("/include/context/extension"):
    if (str(extension.get('name'))=="Forbidden"):
        extension.getparent().remove(extension)        
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        con.api("reloadxml")
    if (str(extension.get('name'))=="Service_Unavailable"):
        extension.getparent().remove(extension)        
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        con.api("reloadxml")
    if (str(extension.get('name'))=="Busy_Here"):
        extension.getparent().remove(extension)        
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        con.api("reloadxml")
d["delnumber"]= "done"

print d


