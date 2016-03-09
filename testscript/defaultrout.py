import os
d = {}
testroute=os.popen("route -v") 
route=testroute.read()
testroute.close()
test="default" in route
if test==True:
    d["route"] = "True"
else:
    d["route"] = "False"
print d
