#!/usr/bin/python
import pexpect
from pexpect import ExceptionPexpect, TIMEOUT, EOF, pxssh
import getpass
import sys
def get_cpu():
    try:
        s = pxssh.pxssh()
        s.login ("192.168.3.6","amani", "amani")
        s.sendline("python /home/amani/testscript/cpu.py")   # run a command
        s.prompt()             # match the prompt
        message=s.before          # print everything before the prompt.
        s.sendline ('exit')
        s.logout()
        return message
    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
        return 0

