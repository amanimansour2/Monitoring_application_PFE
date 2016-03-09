#!/usr/bin/python
import iptc
d={}
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

