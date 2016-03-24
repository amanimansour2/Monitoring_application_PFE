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
print d
