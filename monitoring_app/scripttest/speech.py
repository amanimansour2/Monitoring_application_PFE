#!/usr/bin/python
import os
import sys
d={}
argv1=sys.argv[1]
ch1=os.popen("./pcap_wav.sh "+ argv1)
ch=ch1.read()
ch1.close()
ch=ch.replace("\n"," ")
d["wavname"]=ch
print d
