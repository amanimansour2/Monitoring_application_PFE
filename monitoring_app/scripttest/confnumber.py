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
ch1=sys.argv[1]
point=ch1.find("=")
adsrc=ch1[:point]
ch1=ch1[point+1:len(ch1)]
point=ch1.find("=")
numero=ch1[:point]
ch1=ch1[point+1:len(ch1)]
point=ch1.find("=")
codec=ch1[:point]
file=ch1[point+1:len(ch1)]
timeappel="30"
timerepondeur="20"
path_to_wav="/home/amani/projet/PFE/audio/"+file
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
ch=''

for context in tree.xpath("/include/context"): 
    for extension in tree.xpath("/include/context/extension"):                           
        ch+=str(extension.get('name'))
    if ("conf_test_number_to_gateway_"+numero in ch)==False:
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        y=etree.XML('<extension />')
        y.set('name',"conf_test_number_to_gateway_"+numero)
        context.insert(1,y)
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        if con.connected():
            con.api("reloadxml")
        for extension in tree.xpath("/include/context/extension"):              
            ext=extension.get('name')
            if str(ext)=="conf_test_number_to_gateway_"+numero :
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<condition field="destination_number"/>')
                y.set('expression',"^("+numero+")$")
                l1=etree.XML('<action application="set"/>')
                l1.set('data',"continue_on_fail=true")
                y.append(l1)
                l2=etree.XML('<action application="ring_ready"/>')		        
                
                l6=etree.XML('<action application="set"/>')
                l6.set('data',"ignore_early_media=false")
                y.append(l6)
                l8=etree.XML('<action application="set"/>')
                l8.set('data',"hangup_after_bridge=true")
                y.append(l8)

                l10=etree.XML('<action application="bridge"/>')
                l10.set('data',"{leg_timeout="+timeappel+"}sofia/gateway/gateway_to_"+numero+"/"+numero)
                y.append(l10)
                extension.append(y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                con.api("reloadxml")
    
    if ("conf_test_number_in_gateway_"+numero in ch)==False:
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        y=etree.XML('<extension />')
        y.set('name',"conf_test_number_in_gateway_"+numero)
        context.insert(1,y)
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        if con.connected():
            con.api("reloadxml")
        for extension in tree.xpath("/include/context/extension"):              
            ext=extension.get('name')
            if str(ext)=="conf_test_number_in_gateway_"+numero :
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<condition field="destination_number"/>')
                y.set('expression',"^("+numero+")$")
                l1=etree.XML('<action application="export"/>')
                l1.set('data',"dialed_extension=$1")
                y.append(l1)
                l2=etree.XML('<action application="ring_ready"/>')		        
                y.append(l2)
                l3=etree.XML('<action application="sleep"/>')
                l3.set('data',"10000")
                y.append(l3)
                l5=etree.XML('<action application="answer"/>')		        
                y.append(l5)
                l99=etree.XML('<action inline="true" application="set"/>')
                l99.set('data',"originator_codec="+codec)
                y.append(l99)
				
                l13=etree.XML('<action application="playback"/>')
                l13.set('data',path_to_wav)
                y.append(l13)
                l11=etree.XML('<action application="answer"/>')
                y.append(l11)
                extension.append(y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
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
	
page =etree.Element('include')
doc = etree.ElementTree(page)
pageElement1 = etree.SubElement(page, 'gateway', name="gateway_to_"+numero+".xml")
pageElement2 = etree.SubElement(pageElement1, 'param' ,name='proxy',value=adsrc)
pageElement3 = etree.SubElement(pageElement1, 'param' ,name='username',value=numero)
pageElement4 = etree.SubElement(pageElement1, 'param' ,name='password',value='$${default_password}')
pageElement5 = etree.SubElement(pageElement1, 'param' ,name='register',value="true")
f=open("/usr/local/freeswitch/conf/sip_profiles/external/"+"gateway_to_"+numero+".xml","w") 
doc.write(f, pretty_print=True) 
if con.connected():
    con.api("sofia ","profile external restart reloadxml")
con.api("sofia"," profile external restart reloadxml")
con.api("reloadxml") 
d["statnumber"]= "done"

print d


