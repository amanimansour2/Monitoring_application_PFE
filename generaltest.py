#!/usr/bin/python
import os
import sys
d={}
ch1=os.popen("tc qdisc show dev enp0s8")
ch=ch1.read()
ch1.close()
a="delay" in ch
b="ms" in ch

ch2=os.popen("tc qdisc show dev enp0s3")
chh=ch2.read()
ch2.close()
aa="delay" in chh
bb="ms" in chh

if (a==b==True)or (aa==bb==True):
    d["delay"]="True"
else:
    d["delay"]="False"
testsizev=os.popen("find /var -size  +500M")
sizev=testsizev.read()
testsizev.close()
testsizeh=os.popen("find /home -size  +500M")
sizeh=testsizeh.read()
testsizeh.close()
testsizeu=os.popen("find /usr -size  +500M")
sizeu=testsizeu.read()
testsizeu.close()
if sizeu==sizev==sizeh=="":
    d["volfile"] = "False"
else:
    d["volfile"] = "True"
dhcp=os.popen("netstat -nl |grep :67 ")
dhcps=dhcp.read()
dhcp.close()
if dhcps=='':
    d["dhcpstatus"] = "OFF"
else:
    d["dhcpstatus"] = "ON "
dns=os.popen("netstat -nl |grep :53 ")
dnss=dns.read()
dns.close()
if dnss=='':
    d["dnsstatus"] = "OFF"
else:
    d["dnsstatus"] = "ON "
ntp=os.popen("netstat -nl |grep :123")
ntps=ntp.read()
ntp.close()
if ntps=='':
    d["ntpstatus"] = "OFF"
else:
 d["ntpstatus"] = "ON "
free1=os.popen("netstat -nl |grep :5060 ")
free2=os.popen("netstat -nl |grep :5070 ")
free3=os.popen("netstat -nl |grep :5080 ")
frees1=free1.read()
free1.close()
frees3=free3.read()
free3.close()
frees2=free2.read()
free2.close()
if (frees1=='') or (frees2=='') or(frees3==''):
    d["freestatus"] = "OFF"
else:
    d["freestatus"] = "ON "
usage=os.popen("df /dev/sda1 |tail -n 1")
disk=usage.read()
usage.close()
ch= disk.split()
i=ch[4].replace("%","")
valint=float(i)
if valint < 75 :
    d["disk"]="Secure"
else:
    d["disk"]="Risky"
testroute=os.popen("route -v")
route=testroute.read()
testroute.close()
test="default" in route
if test==True:
    d["route"] = "True"
else:
    d["route"] = "False"
cpur=os.popen("mpstat |tail -n 1")
cpu=cpur.read()
cpur.close()
cpus=cpu.split()
cpsys=cpus[4]
cpuser=cpus[2]
cpsys=cpsys.replace(",",".")
cpuser=cpuser.replace(",",".")
i=float(cpsys)+float(cpuser)
ss=str(i)
d["cpu"] = ss+" %"
table = iptc.Table(iptc.Table.FILTER)
chain = iptc.Chain(table, "INPUT")
l1=len(chain.rules)
chain = iptc.Chain(table, "OUTPUT")
l2=len(chain.rules)
chain = iptc.Chain(table, "FORWARD")
l3=len(chain.rules)
if l1==l2==l3==0:
    d["firewall"]="False"
else:
    d["firewall"]="True"

print d
