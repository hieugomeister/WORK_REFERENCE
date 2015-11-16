'''
Nexus movie: 0_buycdmn8_0_dpdnx663_2.mp4
Format: 480p/60fps
Date: Feb 13, 2015
File name: ssh_nexus_480p.py

'''

import os
import sys
import time
import logging
import pexpect
import subprocess
import re



print "Running Test... please wait."


#host = sys.argv[1]

try:
    #command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + host
    command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + '192.168.1.206'
    session = pexpect.spawn(command)
    session.expect('password: ')
    session.sendline('verizon123')
    session.expect _exact('# ')
    session.sendline('su -')
    session.expect('# ')
    session.sendline('cd ..')
    session.expect('# ')
    session.sendline('mount 192.168.1.205:/tftpboot /mnt/nfs')
    session.expect('# ')
    session.sendline('cd /mnt/nfs/bin')
    session.expect('# ')
    session.sendline('pwd')
    session.expect('# ')  
    session.sendline('killall nxserver')
    session.expect('# ')
    print 'nx server killed'
    time.sleep(2)
    session.sendline('nexus.client play ../0_buycdmn8_0_dpdnx663_2.mp4')
    session.expect('playback>')
    print 'play command sent'
    time.sleep(133)
    session.sendline('quit')
    session.expect('# ')
    print 'End of nexus'
    
except:
    print "Not working"
    

