'''
Program to play all the movies autonomously
and wait 5 minutes in each mive to give the tester
enough time to test for the Input/Output audio and
video performance of the STB. User can hit enter to
stop at any time
File name: TBD

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

def LogIn(session):
    session.expect('password: ') #Now session is created                   
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

def RunNexus(session):
    session.sendline('killall nxserver')
    session.expect('# ')
    print('nx server killed')
    time.sleep(3)
    session.sendline('./nexus nxserver &')
    time.sleep(2)
    

def PlayMovies(session, Command):           
    session.sendline(Command)
    print('Play command sent. Please perform Audio and Video tests'+'\n')
    print('You have 3 minutes\n')
    
    for t in xrange(120,-1,-1):
        minutes = (t / 60)
        seconds = (t % 60)        
        print('\rPlaying movie [%d:%2d]'%(minutes,seconds))        
        time.sleep(1.0)             #every second, for 5 minutes

    session.send(chr(3))            #Send a Ctrl+C  
    session.sendline('\n')          #Send a CR
    session.expect('# ')       

def AllDone(session):
    session.sendline('reboot')
    time.sleep(60)
    session.sendline('\n')
    session.expect('# ')
    print('End of nexus')
    

                                    #print "Running Test... please wait."

                                    #filename = sys.argv[2]
filename = '0_buycdmn8_0_dpdnx663_2.mp4'
host = '192.168.1.171'
#host = '192.168.1.174'
                                    #host = sys.argv[1]

try:
    #session = pxssh.pxssh()
    command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + host)
    session = pexpect.spawn(command) #Instantiates an object of pexpect class called session
    LogIn(session)
    RunNexus(session)
    print('Play Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4  tile\n')
    print('Resolution is: 4K\n')
    cmmnd = ('./nexus.client play ../movies/Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4')
    PlayMovies(session,cmmnd)
    print('Play e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4 tile\n')
    print('Resolution is: 1080p, generic\n')
    cmmnd = ('./nexus.client play ../movies/e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4')
    PlayMovies(session,cmmnd)
    print('Play Inception_TRLR3_720.mp4 tile\n')
    print('Resolution is: generic 720p\n')
    cmmnd = ('./nexus.client play ../movies/Inception_TRLR3_720.mp4')
    PlayMovies(session,cmmnd)
    print('Play generic 480p clip\n')
    print('Resolution is: 480p, generic\n')
    cmmnd = ('./nexus.client play ../movies/0_buycdmn8_0_dpdnx663_2.mp4')
    PlayMovies(session,cmmnd)    
    AllDone(session)    
except:
    print("Not working")
    print(session.before)
    print(session.after)
    

