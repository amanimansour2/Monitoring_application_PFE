from lxml import etree
import ESL
import sys 
adsrc=sys.argv[1]#"192.168.3.5"
addest=sys.argv[2]#"192.168.3.6"
prefixsrc=sys.argv[3]#0
prefixdest=sys.argv[4]#1
nomsrc=sys.argv[5]#"BoxA"
nomdest=sys.argv[6]#"BoxB"
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl")
    con.api("reloadxml")
#autoriser le domaine du freeswitch destinataire 
tree = etree.parse('/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml')
ch=''
for list in tree.xpath("/configuration/network-lists/list"):              
    p=list.get('name')
    if str(p)=="domains" :
        for node in tree.iter("node"):
			ch+= str(node.attrib)
        if (addest in ch)== False :
            f = open('/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml', 'w')
            y=etree.XML('<node type="allow"/>')
            y.set('cidr',addest+"/32")
            list.append(y)
            f.write(etree.tostring(tree, pretty_print=True))
            f.close()
#acheminer les appels entrants au freeswitch .5 commancant par +prefixsrc    
tree = etree.parse('/usr/local/freeswitch/conf/dialplan/default.xml')
ch=''
for context in tree.xpath("/include/context"): 
    for extension in tree.xpath("/include/context/extension"):                           
        ch+=str(extension.get('name'))
    if ("Dial to "+nomdest in ch)==False:
        f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
        y=etree.XML('<extension />')
        y.set('name',"Dial to "+nomdest)
        context.insert(1,y)
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        if con.connected():
            con.api("reloadacl")
            con.api("reloadxml")
        for extension in tree.xpath("/include/context/extension"):              
            ext=extension.get('name')
            if str(ext)=="Dial to "+nomdest :
                f = open('/usr/local/freeswitch/conf/dialplan/default.xml', 'w')
                y=etree.XML('<condition field="destination_number"/>')
                y.set('expression',"^\+"+str(prefixdest)+"(\d\d\d\d)$")
                x=etree.XML('<action application="bridge"/>')
                x.set('data',"sofia/internal/$1@"+addest)
                y.append(x)
                extension.append(y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()
 #acheminer les appels sortants au freeswitch .5 commancant par +prefixsrc    
tree = etree.parse('/usr/local/freeswitch/conf/dialplan/public.xml')
ch=''
for context in tree.xpath("/include/context"): 
    for extension in tree.xpath("/include/context/extension"):                           
        ch+=str(extension.get('name'))
    if ("Calls from "+nomdest in ch)==False:
        f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
        y=etree.XML('<extension />')
        y.set('name',"Calls from "+nomdest)
        context.append(y)
        f.write(etree.tostring(tree, pretty_print=True))
        f.close()
        if con.connected():
            con.api("reloadacl")
            print "cccccccccccccccccc"
            con.api("reloadxml")
        for extension in tree.xpath("/include/context/extension"):              
            ext=extension.get('name')
            if str(ext)=="Calls from "+nomdest :
                f = open('/usr/local/freeswitch/conf/dialplan/public.xml', 'w')
                y=etree.XML('<condition field="destination_number"/>')
                y.set('expression',"^\+"+str(prefixsrc)+"(\d\d\d\d)$")
                x=etree.XML('<action application="transfer"/>')
                x.set('data',"$1 XML default")
                y.append(x)
                extension.append(y)
                f.write(etree.tostring(tree, pretty_print=True))
                f.close()

if con.connected():
    con.api("reloadacl")
    con.api("reloadxml")
    

