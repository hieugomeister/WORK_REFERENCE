'''
Nexus movie: Inception_TRLR3_720.mp4
Format: 720p/60fps
Date: Feb 13, 2015
File name: ssh_nexus_argv.py

'''

#!/usr/bin/env python

import os
import re
import sys
import time
import logging
import pxssh
import pexpect
import optparse
import getpass
import subprocess
import traceback



def die(session, errstr):
    print errstr
    print session.before, session.after
    session.terminate()
    exit(1)


print "Running Test... please wait."

#filename = sys.argv[2]
filename = '0_buycdmn8_0_dpdnx663_2.mp4'
host = '192.168.1.155'
#host = sys.argv[1]

try:
    #session = pxssh.pxssh()
    command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + host
    session = pexpect.spawn(command)
    session.expect('password: ')
                   
    #if i == 0:
    #    die(session, 'ERROR!\nSSH timed out. Here is what SSH said:')
    #elif i == 1:
    #    die(session, 'ERROR!\nIncorrect password Here is what SSH said:')
    #elif i == 2:
    #    print session.before
                   
    session.sendline('verizon123')
    session.expect_exact('# ')
    session.sendline('su -')
    session.expect('# ')
    session.sendline('cd ..')
    session.expect('# ')
    session.sendline('mount 192.168.1.167:/tftpboot /mnt/nfs') #Mine is at this location
    session.expect('# ')
    session.sendline('cd /mnt/nfs/bin')
    session.expect('# ')
    session.sendline('pwd')
    session.expect('# ')  
    session.sendline('killall nxserver')
    session.expect('# ')
    print('nx server killed')
    time.sleep(3)
    session.sendline('./nexus nxserver &')
    time.sleep(2)
    #session.sendline('ls nexus')
    #session.prompt()
    #str2 = session.before
    #print(str2)
    #print('Playing back movie clip: ' + filename)                   
    #session.expect('# ')
    #print('nx server killed')
    #time.sleep(2)
    session.sendline('./nexus.client play ../movies/0_buycdmn8_0_dpdnx663_2.mp4')
    #session.expect('playback> ')
    print('play command sent')
    time.sleep(54000)
    session.send(chr(3))    
    session.sendline('\n')
    session.sendline('reboot')
    time.sleep(60)
    session.sendline('\n')
    session.expect('# ')
    print('End of nexus')
    
except:
    print("Not working")
    print(session.before)
    print(session.after)
    

