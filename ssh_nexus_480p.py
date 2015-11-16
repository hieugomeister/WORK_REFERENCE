'''
Nexus movie: 0_buycdmn8_0_dpdnx663_2.mp4
Format: 480p/60fps
Date: Feb 13, 2015
File name: ssh_nexus_480p.py
Execution Cmd: python ssh_nexus_480p.py <Mallard IP address>

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
    print 'nx server killed'
    time.sleep(2)
    session.sendline('nexus playback ../0_buycdmn8_0_dpdnx663_2.mp4')
    session.expect('playback>')
    print 'play command sent'
    time.sleep(133)
    session.sendline('quit')
    session.expect('# ')
    print 'End of nexus'
    
except:
    print "Not working"
    

