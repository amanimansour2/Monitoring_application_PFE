#!/usr/bin/python
from lxml import etree
import ESL
import sys 
import json
import ast
d={}
adsrc=sys.argv[2]
l=ast.literal_eval(sys.argv[1])
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
#autoriser le domaine du freeswitch destinataire (votre freeswitch est celui qui a @IP adsrc)
i=0
while i < n :
    if l[i][0] != adsrc :
	    tree = etree.parse('/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml')
		ch=''
		for list in tree.xpath("/configuration/network-lists/list"):              
		    p=list.get('name')
		    if str(p)=="domains" :
			for node in tree.iter("node"):
					ch+= str(node.attrib)
			if (l[i][0] in ch)== False :
			    f = open('/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml', 'w')
			    y=etree.XML('<node type="allow"/>')
			    y.set('cidr',l[i][0]+"/32")
			    list.append(y)
			    f.write(etree.tostring(tree, pretty_print=True))
			    f.close()
    i=i+1
#acheminer les appels entrants au freeswitch adsrc
i=0
while i < n :
   if l[i][0] != adsrc :   
        tree = etree.parse('/usr/local/freeswitch/conf/dialplan/default.xml')
		ch=''
		for context in tree.xpath("/include/context"): 
		    for extension in tree.xpath("/include/context/extension"):                           
			ch+=str(extension.get('name'))
		    if ("Dial to "+l[i][0] in ch)==False:
			f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
			y=etree.XML('<extension />')
			y.set('name',"Dial to "+l[i][0])
			context.insert(1,y)
			f.write(etree.tostring(tree, pretty_print=True))
			f.close()
			if con.connected():
			    con.api("reloadacl")
			    con.api("reloadxml")
			for extension in tree.xpath("/include/context/extension"):              
			    ext=extension.get('name')
			    if str(ext)=="Dial to "+l[i][0] :
				f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
				y=etree.XML('<condition field="destination_number"/>')
				y.set('expression',"^\+"+l[i][1]+"(\d\d\d\d)$")
				x=etree.XML('<action application="bridge"/>')
				x.set('data',"sofia/internal/$1@"+l[i][0])
				y.append(x)
				extension.append(y)
				f.write(etree.tostring(tree, pretty_print=True))
				f.close()
	i=i+1
#acheminer les appels sortants au freeswitch dont l'adresse est adsrc commancant par l[adsrc][1]   
i=0
while i < n :
    if l[i][0] == adsrc :
		tree = etree.parse('/usr/local/freeswitch/conf/dialplan/public.xml')
		ch=''
		for context in tree.xpath("/include/context"): 
		    for extension in tree.xpath("/include/context/extension"):                           
			ch+=str(extension.get('name'))
		    if ("Calls go to "+adsrc in ch)==False:
			f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
			y=etree.XML('<extension />')
			y.set('name',"Calls go to "+adsrc)
			context.append(y)
			f.write(etree.tostring(tree, pretty_print=True))
			f.close()
			if con.connected():
			    con.api("reloadacl")
			    con.api("reloadxml")
			for extension in tree.xpath("/include/context/extension"):              
			    ext=extension.get('name')
			    if str(ext)=="Calls go to "+adsrc :
				f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
				y=etree.XML('<condition field="destination_number"/>')
				y.set('expression',"^\+"+l[i][1]+"(\d\d\d\d)$")
				x=etree.XML('<action application="transfer"/>')
				x.set('data',"$1 XML default")
				y.append(x)
				extension.append(y)
				f.write(etree.tostring(tree, pretty_print=True))
				f.close()
    i=i+1
if con.connected():
    con.api("reloadacl")
    con.api("reloadxml")
d["stat"]="done"
print d
        

