#!/usr/bin/python
from lxml import etree
import xml.etree.ElementTree
import lxml.etree
from StringIO import StringIO
import os
import ESL
import pexpect
import subprocess
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
import json
from lxml.builder import E
import sys 
import time
import json
import ast
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
d={}


adsrc=sys.argv[1]
numsrc=sys.argv[2]
numdest=sys.argv[3]
scenarioinvite=sys.argv[4]
con.api("originate", "sofia/gateway/gateway_to_%s.xml/%s &park()" %(numsrc,numdest))
if con.connected():
    con.api("reloadxml")
time.sleep(1)
d["statnumber"]= "done"

print d


