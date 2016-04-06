#!/usr/bin/python
import subprocess as sub
import sys
pcap=sys.argv[1]
law='a-law'


p = sub.Popen(('sudo', 'tshark','-n','-r',pcap,'-Y','rtp'),stdout=sub.PIPE)
i=p.stdout.read()
l=[]
j=0

k=len(i)
ni=i.count("SSRC")
h=0
while h<ni:
    q=0
    q1=0
    q=i.find('SSRC')
    i=i[q:len(i)]
    d=i.find('=')
    i=i[d+1:len(i)]
    q1=i.find(',')
    l+=[i[:q1]]
    i=i[q1+1:len(i)]
    j=j+q+q1+1
    h+=1
pa=[]
w=0
v=0
if( len(l)>=1):
    elem=l[0]
    v=1
    pa+=["ssrc"+str(v)+"="+str(elem)]
liste=[elem]
while w<len(l):
    if ((l[w] in liste)==False) or(l[w]=='') :
        liste+=[l[w]]
        v+=1
        pa+=["ssrc"+str(v)+"="+str(l[w]) ]      
    w+=1
print pa
