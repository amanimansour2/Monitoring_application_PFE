import os
dict_data = {}
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
dict_data["cpu"] = ss+" %"
print dict_data

