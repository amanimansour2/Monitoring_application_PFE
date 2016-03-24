import ESL
import sys
address="127.0.0.1"
port="8021"
auth="ClueCon"
command="sofia status profile internal reg"
d={}
con =ESL.ESLconnection(address,port,auth)
if con.connected():
    e = con.api(command)
    ch=e.getBody()
    pos=ch.find("Total items returned")
    i=pos+len("Total items returned")
    nombre=ch[i+2:i+3]
    ch1=ch
    j=0
    p=0
    number_ch = ""
    while j<int(nombre):
        j=j+1
        k=ch1.find("Auth-User:")
        p=p+k+len("Auth-User:")+3
        # number can be more tha 4 digits
        ch1=ch[p:]
        if j== int(nombre):
             number_ch += ch[p:p+4]
        else :
             number_ch +=  ch[p:p+4]+ "--"
    d["phone"]=number_ch
else:
    print "Not Connected"
    sys.exit(2)
print d

