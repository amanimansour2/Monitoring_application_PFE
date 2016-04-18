#!/usr/bin/python
import os
import ESL
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
from shutil import copyfile
from distutils.dir_util import copy_tree
import shutil 
import json
import sys 
import time
import json
con=ESL.ESLconnection("127.0.0.1","8021","ClueCon")
con.api("sofia","profile external restart")
time.sleep(3)
con.api("sofia","profile external killgw _all_")
time.sleep(2)
user=sys.argv[1]
copyfile('/home/%s/FSinitial/default.xml' %(user),'/usr/local/freeswitch/conf/dialplan/default.xml')
copyfile('/home/%s/FSinitial/public.xml' %(user),'/usr/local/freeswitch/conf/dialplan/public.xml')
copyfile('/home/%s/FSinitial/acl.conf.xml' %(user),'/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml')
shutil.rmtree('/usr/local/freeswitch/conf/directory/default/')
copy_tree('/home/%s/FSinitial/default' %(user), '/usr/local/freeswitch/conf/directory/default')
shutil.rmtree('/usr/local/freeswitch/conf/sip_profiles/external/')
copy_tree('/home/%s/FSinitial/external' %(user), '/usr/local/freeswitch/conf/sip_profiles/external')
d={}
if con.connected():
    con.api("reloadacl") 
    con.api("reloadxml")
	
d["initialisation"]= "done"

print d
