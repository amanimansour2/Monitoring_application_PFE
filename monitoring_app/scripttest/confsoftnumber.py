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
import time
from lxml.builder import E
import sys 
import json
import ast
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
ch=''
d={}
adsrc=sys.argv[1]
numero=sys.argv[2]
scenario=sys.argv[3]
timerecord=sys.argv[4]
msgrecord=sys.argv[5]
adphone=sys.argv[6]
dtmf=sys.argv[7]
selecteddd=sys.argv[8]

print msgrecord
testexistnumber="|"+numero
tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
if (scenario=="Unauthorize"):
    number="1"
    SIPP1_IP=adsrc
    SIPP1_PORT="5061"
    SIPP2_PORT=adphone
    os.chdir('/usr/src/sipp.svn') 
    ch1="#!/usr/bin/python/ \nimport os \nimport time \nos.system(\"iptables -t nat -A POSTROUTING  -p udp -s %s --sport %s -j SNAT --to  %s:5060\") \nos.system(\" iptables -t nat -A PREROUTING  -p udp -s %s --dport 5060 -j DNAT --to-destination  %s:%s \")  \nos.system(\"./sipp -sf testregister.xml -m %s\")\nos.system(\" iptables -F \") \nos.system(\"iptables -X \") \nos.system(\" iptables -t nat -F \") \nos.system(\" iptables -t nat -X \") \nos.system(\" iptables -t mangle -F \")\nos.system(\" iptables -t mangle -X \") \nos.system(\"iptables -P INPUT ACCEPT \") \nos.system(\" iptables -P OUTPUT ACCEPT \") \nos.system(\"iptables -P FORWARD ACCEPT \") \nos.system(\"iptables -t nat -L\")" %(adsrc,SIPP1_PORT,SIPP1_IP,SIPP2_PORT,SIPP1_IP,SIPP1_PORT,number)
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
if (selecteddd=='YES'):
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    ch=''
    for context in tree.xpath("/include/context"): 
        for extension in tree.xpath("/include/context/extension"):                           
            ch+=str(extension.get('name'))
        if ("DTMF_FOR_"+numero in ch)==False:
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            y=etree.XML('<extension />')
            y.set('name',"DTMF_FOR_"+numero)
            context.insert(1,y)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()
            if con.connected():
                con.api("reloadxml")
            for extension in tree.xpath("/include/context/extension"):              
                ext=extension.get('name')
                if str(ext)=="DTMF_FOR_"+numero :
                    f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                    y=etree.XML('<condition field="destination_number"/>')
                    y.set('expression',"^("+numero+")$")
                    l1=etree.XML('<action application="export"/>')
                    l1.set('data',"dialed_extension=$1")
                    y.append(l1)
                    l2=etree.XML('<action application="set"/>')
                    l2.set('data',"ringback=${us-ring}")
                    y.append(l2)
                    l3=etree.XML('<action application="set"/>')
                    l3.set('data',"transfer_ringback=$${hold_music}")
                    y.append(l3)
                    l4=etree.XML('<action application="set"/>')
                    l4.set('data',"call_timeout=40")
                    y.append(l4)
                    l5=etree.XML('<action application="set"/>')
                    l5.set('data',"hangup_after_bridge=true")
                    y.append(l5)
                    l6=etree.XML('<action application="set"/>')
                    l6.set('data',"continue_on_fail=true")
                    y.append(l6)
                    l7=etree.XML('<action application="queue_dtmf"/>')
                    l7.set('data',dtmf)
                    y.append(l7)
                    l6=etree.XML('<action application="set"/>')
                    l6.set('data',"ignore_early_media=false")
                    y.append(l6)
                    l10=etree.XML('<action application="bridge"/>')
                    l10.set('data',"user/${dialed_extension}@${domain_name}")
                    y.append(l10)
                    l11=etree.XML('<action application="answer"/>')		        
                    y.append(l11)
                    extension.append(y)
                    f.write(etree.tostring(tree, pretty_print=True))
                    f.close()
                    con.api("reloadxml")
				
if (scenario=="None")or(scenario=="Forbidden")or (scenario=="Service_Unavailable")or(scenario=="Busy_Here"):
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))=="Local_Extension":
            c=extension.find('condition').get('expression')      
            n1="|"+numero+"|"
            n2="|"+numero+")"		
            if ((n1 in c)==False) and ((n2 in c)==False) :  		           
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                r=c.replace(")","|"+numero+")")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                if con.connected():
                    con.api("reloadxml")
    if selecteddd=="NO":
        for extension in tree.xpath("/include/context/extension"):
            if str(extension.get('name'))=="DTMF_FOR_"+numero:
                extension.getparent().remove(extension)        
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                con.api("reloadxml")
    if scenario=="None":
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for extension in tree.xpath("/include/context/extension"):
            if str(extension.get('name'))=="Forbidden":
                c=extension.find('condition').get('expression')             
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                r=c.replace(testexistnumber,"")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                con.api("reloadxml")
            if str(extension.get('name'))=="Service_Unavailable":
                c=extension.find('condition').get('expression')             
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                r=c.replace(testexistnumber,"")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                con.api("reloadxml")
            if str(extension.get('name'))=="Busy_Here":
                c=extension.find('condition').get('expression')             
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                r=c.replace(testexistnumber,"")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/public.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))=="public_extensions":
            c=extension.find('condition').get('expression')            
            n1="|"+numero+"|"
            n2="|"+numero+")"		
            if ((n1 in c)==False)and ((n2 in c)==False) :               
                f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
                r=c.replace(")","|"+numero+")")
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
if con.connected():
    con.api("reloadxml") 		
testnumber=False
testscenario=False
scenarioname="None"

tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
for context in tree.xpath("/include/context"):
    for extension in tree.xpath("/include/context/extension"):                           
        ch+=str(extension.get('name'))
    if (scenario in ch)==True:
        testscenario=True

tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
for extension in tree.xpath("/include/context/extension"):
    if (str(extension.get('name'))=="Forbidden"):
        c=extension.find('condition').get('expression')            
        if ((testexistnumber+")" in c)==True) or ((testexistnumber+"|" in c)==True): 
            testnumber=True
            scenarioname="Forbidden"
    if (str(extension.get('name'))=="Service_Unavailable"):
        c=extension.find('condition').get('expression')            
        if ((testexistnumber+")" in c)==True) or ((testexistnumber+"|" in c)==True): 
            testnumber=True
            scenarioname="Service_Unavailable"
    if (str(extension.get('name'))=="Busy_Here"):
        c=extension.find('condition').get('expression')            
        if ((testexistnumber+")" in c)==True) or ((testexistnumber+"|" in c)==True): 
            testnumber=True
            scenarioname="Busy_Here"

if (testscenario ==False) and (testnumber == False) :
    if scenario=="Forbidden" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Forbidden" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Forbidden")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Forbidden" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"403")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")

    if scenario=="Service_Unavailable" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Service_Unavailable" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Service_Unavailable")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Service_Unavailable" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"503")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")

    if scenario=="Busy_Here" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Busy_Here" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Busy_Here")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Busy_Here" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"486")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")
elif (testscenario==False)and(testnumber==True):
    if scenario=="Forbidden" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Forbidden" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Forbidden")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Forbidden" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"403")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))==scenarioname:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c.replace(testexistnumber,"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
    if scenario=="Service_Unavailable" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Service_Unavailable" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Service_Unavailable")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Service_Unavailable" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"503")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))==scenarioname:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c.replace(testexistnumber,"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")

    if scenario=="Busy_Here" :
        tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
        for context in tree.xpath("/include/context"): 
            for extension in tree.xpath("/include/context/extension"):                           
                ch+=str(extension.get('name'))
            if ("Busy_Here" in ch)==False:
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<extension />')
                y.set('name',"Busy_Here")
                context.insert(1,y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
                if con.connected():
                    con.api("reloadxml")
                for extension in tree.xpath("/include/context/extension"):              
                    ext=extension.get('name')
                    if str(ext)=="Busy_Here" :
                        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                        y=etree.XML('<condition field="caller_id_number"/>')
                        y.set('expression',"^(|"+numero+")$")
                        l1=etree.XML('<action application="respond"/>')
                        l1.set('data',"486")
                        y.append(l1)                
                        l6=etree.XML('<action application="hangup"/>')
                        y.append(l6)
                        extension.append(y)
                        f.write(etree.tostring(tree, pretty_print=True))
                        f.close()
                        con.api("reloadxml")
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))==scenarioname:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c.replace(testexistnumber,"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
elif (testscenario==True)and(testnumber==True):
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))==scenarioname:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            r=c.replace(testexistnumber,"")
            extension.find('condition').set('expression',r)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()	
            con.api("reloadxml")
        if str(extension.get('name'))==scenario:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            if ((testexistnumber+")" in c)==False) and ((testexistnumber+"|" in c)==False): 
                r=c.replace(")","|"+numero+")")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                con.api("reloadxml")
elif (testscenario==True)and(testnumber==False):
    tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    for extension in tree.xpath("/include/context/extension"):
        if str(extension.get('name'))==scenario:
            c=extension.find('condition').get('expression')             
            f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
            if ((testexistnumber+")" in c)==False) and ((testexistnumber+"|" in c)==False): 
                r=c.replace(")","|"+numero+")")
                extension.find('condition').set('expression',r)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()	
                con.api("reloadxml")
    # j=0
    # l=0
    # tree = etree.parse("/usr/local/freeswitch/conf/dialplan/default.xml")
    # for extension in tree.xpath("/include/context/extension/condition/action"):
        # if str(extension.getparent().getparent().get('name'))=="Local_Extension":
            # j=j+1
    # for extension in tree.xpath("/include/context/extension/condition/action"):
        # if str(extension.getparent().getparent().get('name'))=="Local_Extension":
            # l=l+1
            # if l==(j-4) :
                # f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                # y=etree.XML('<condition field="destination_number"/>')
                # y.set('expression',"^(1500)$")
                # y1=etree.XML('<action application="queue_dtmf"/>')
                # y1.set('data',"1234568")
                # y.append(y1)


                # extension.insert(l,y)
                # f.write(etree.tostring(tree, pretty_print=True))
                # f.close()
                # con.api("reloadxml")
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
time.sleep(1)
d["statnumber"]= "done"
print d