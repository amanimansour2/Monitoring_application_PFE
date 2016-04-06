#!/usr/bin/python
import subprocess as sub
import time
import psutil
from subprocess import Popen, PIPE
import sys
PROCNAME = "tcpdump"
name=sys.argv[1]
p = sub.Popen(('sudo', 'tcpdump','-i','enp0s8','-n',' udp ','-w','/home/amani/'+name),stdout=sub.PIPE)
time.sleep(20)
p.stdout.close()
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
print("cccc")
