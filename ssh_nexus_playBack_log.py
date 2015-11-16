'''
Nexus movie: ????.mp4
Format: Any
Date: Feb 16, 2015
File name: ssh_nexus_playBack_log.py
Execution Cmd: python ssh_nexus_playBack_log.py <Mallard IP address> <Movie.mp4>

'''

import os
import sys
import time
import logging
import pexpect
import subprocess
import re



print "Running Test... please wait."


host = sys.argv[1]
fileName = sys.argv[2]

try:
    command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + host
    session = pexpect.spawn(command)
    session.expect('password: ')
    session.sendline('verizon123')
    session.expect_exact('# ')
    session.sendline('su -')
    session.expect('# ')
    session.sendline('cd ..')
    session.expect('# ')
    session.sendline('mount 192.168.1.207:/tftpboot /data/videos')
    session.expect('# ')
    session.sendline('cd /data/videos/bin')
    session.expect('# ')
    session.sendline('pwd')
    session.expect('# ')  
    session.sendline('killall nxserver')
    session.expect('# ')
    #print 'nx server killed'
    time.sleep(2)
    session.sendline ('nexus playback ../' + fileName)
    session.expect('playback>')
    print 'play command sent'
    #time.sleep(133)
    time.sleep(60)
    session.sendline('quit')
    session.expect('# ')
    print 'End of nexus'
    
except:
    print "Not working"
    

