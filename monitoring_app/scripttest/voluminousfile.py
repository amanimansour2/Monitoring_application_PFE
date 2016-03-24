import os
d = {}
testsizev=os.popen("find /var -size  +500M")
sizev=testsizev.read()
testsizev.close()
testsizeh=os.popen("find /home -size  +500M")
sizeh=testsizeh.read()
testsizeh.close()
testsizeu=os.popen("find /usr -size  +500M")
sizeu=testsizeu.read()
testsizeu.close()
if sizeu==sizev==sizeh=="":
    d["volfile"] = "False"
else:   
    d["volfile"] = "True"
print d
