#!/usr/bin/python
import subprocess as sub
import time
import psutil
from subprocess import Popen, PIPE
import sys
PROCNAME = "tcpdump"
name=sys.argv[1]
timea=sys.argv[2]
user=sys.argv[3]
ch=user+'/'+name
p = sub.Popen(('sudo', 'tcpdump','-i','enp0s8','-n','udp and src host 192.168.3.1','-w','/home/'+ch),stdout=sub.PIPE)
time.sleep(float(timea))
p.stdout.close()
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
print("cccc")
