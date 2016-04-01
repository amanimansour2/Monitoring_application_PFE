import ESL
import sys
address="127.0.0.1"
port="8021"
auth="ClueCon"
command="sofia status profile internal reg"
d={}
d["phone"]="no numbers"
con =ESL.ESLconnection(address,port,auth)
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
b=con.api('sofia','profile external restart')
print b.getBody()
if con.connected():
    c=con.execute("reloadxml")
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
    l=4
    while j<int(nombre):
        j=j+1
        k=ch1.find("Auth-User:")
        p=p+k+len("Auth-User:")+3
		
        # number can be more tha 4 digits
        ch1=ch[p:]
        print ch1 
        if j== int(nombre):
             l=ch1.find("\n")
             number_ch += ch[p:p+l]
             d["phone"]=number_ch
        else :
             l=ch1.find("\n")
             number_ch +=  ch[p:p+l]+ "--"
             d["phone"]=number_ch
else:
    print "Not Connected"
    sys.exit(2)
print d

