import os
d = {}
usage=os.popen("df /dev/sda1 |tail -n 1")
disk=usage.read()
usage.close()
ch= disk.split()
i=ch[4].replace("%","")
valint=float(i)
if valint < 80 :
    d["disk"]="Secure"
else:
    d["disk"]="Risky"
print d
