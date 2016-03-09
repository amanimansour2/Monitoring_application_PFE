import os

dict_data = {}
dhcp=os.popen("netstat -nl |grep :67 ")
dhcps=dhcp.read()
dhcp.close()
if dhcps=='':
    dict_data["dhcpstatus"] = "OFF"
else:
    dict_data["dhcpstatus"] = "ON "
dns=os.popen("netstat -nl |grep :53 ")
dnss=dns.read()
dns.close()
if dnss=='':
    dict_data["dnsstatus"] = "OFF"
else:
    dict_data["dnsstatus"] = "ON "
ntp=os.popen("netstat -nl |grep :123")
ntps=ntp.read()
ntp.close()
if ntps=='':
    dict_data["ntpstatus"] = "OFF"
else:
    dict_data["ntpstatus"] = "ON "
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
    dict_data["freestatus"] = "OFF"
else:
    dict_data["freestatus"] = "ON "

print dict_data
