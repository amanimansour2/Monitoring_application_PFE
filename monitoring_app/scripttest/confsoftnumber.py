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
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
d={}
ch=sys.argv[1]
point=ch.find("=")
adsrc=ch[:point]
numero=ch[point+1:len(ch)]
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
for extension in tree.xpath("/include/context/extension"):
    if str(extension.get('name'))=="Local_Extension":
        c=extension.find('condition').get('expression')      
        n1="|"+numero+"|"
        n2="|"+numero+")"		
        if ((n1 in c)==False)and ((n1 in c)==False) :  		           
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c[:len(c)-2]+"|"+str(numero)+")$"
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            if con.connected():
                con.api("reloadxml")
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/public.xml")
for extension in tree.xpath("/include/context/extension"):
    if str(extension.get('name'))=="public_extensions":
        c=extension.find('condition').get('expression')            
        n1="|"+numero+"|"
        n2="|"+numero+")"		
        if ((n1 in c)==False)and ((n1 in c)==False) :               
            f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
            r=c[:len(c)-2]+"|"+str(numero)+")$"
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            if con.connected():
                con.api("reloadxml")
				
page =etree.Element('include')
doc = etree.ElementTree(page)
pageElement1 = etree.SubElement(page, 'user', id=numero)
pageElement2 = etree.SubElement(pageElement1, 'params')
pageElement3 = etree.SubElement(pageElement2, 'param',name='password',value='$${default_password}')
pageElement4 = etree.SubElement(pageElement2, 'param', name='vm-password', value=numero)	
pageElement5 = etree.SubElement(pageElement1, 'variables')
pageElement6 = etree.SubElement(pageElement5, 'variable',name='toll_allow',value='domestic,international,local')	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='accountcode',value=numero)	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='user_context',value='default')	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='effective_caller_id_name',value='Extension '+numero)	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='effective_caller_id_number',value=numero)	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='outbound_caller_id_name',value='$${outbound_caller_name}')	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='outbound_caller_id_number',value='$${outbound_caller_id}')	
pageElement6 = etree.SubElement(pageElement5, 'variable',name='callgroup',value='techsupport')	
f=open("/usr/local/freeswitch/conf/directory/default/"+numero+".xml","w") 
doc.write(f, pretty_print=True) 
if con.connected():
    con.api("reloadxml") 
d["statnumber"]= "done"

print d


