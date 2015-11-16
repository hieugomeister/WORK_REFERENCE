'''
Program to play preselected movies autonomously
and wait 2 minutes for each movie to play while
the audio and video performance of the STB is validated.

File name: dailytest_ssh.py

'''

#!/usr/bin/env python

import os
import re
import sys
import time
import pexpect
import logging
import getpass
import optparse
import traceback
import subprocess

MiscCmd = 'wificonnect.sh FiOS-OD9CD 5946rescue9135tip'
hostWC = '192.168.1.171'
hostWL = '192.168.1.174'
remoteLoc = '192.168.1.167'

#------------------------------------------------------------
#For wireless, user is expected to have wificonnect.sh
#executed successfully already such that the WLAN0 IpAddress
#is available.
#
#User of the class must pass in the following values
#Channel type:  0 = Wireless lan
#               1 = RJ45 Ethernet
#               2 = MoCA
#The movie title
#Any comment
#------------------------------------------------------------

class TestBox:    
    def __init__(self,InetChannel,MovieToPlay,errstr):
        self.Ichannel = InetChannel
        self.Movie = MovieToPlay
        self.Error = errstr
        SetSession(self.Ichannel) #Set the session based on channel type

    def SetSession(self):
        if self.Ichannel == 0: #WLAN
            self.host = hostWL
            self.command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + self.host)
            self.session = pexpect.spawn(self.command)
        elif self.Ichannel == 1 or self.Ichannel == 2: #RJ45 or MoCA
            self.host = hostWC
            self.command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + self.host)
            self.session = pexpect.spawn(self.command)
            #The constructor will call SetSession() method
            #for subsequent use.
        
    def die(self):
        self.Error = 'Connection problem...'
        print(self.Error)
        print(self.session.before, self.session.after)
        self.session.terminate()
        exit(1)

    def LogIn(self):
        self.session.expect('password: ') #Now session is created                   
        self.session.sendline('verizon123')
        self.session.expect_exact('# ')
        self.session.sendline('su -')
        self.session.expect('# ')
        self.session.sendline('cd ..')
        self.session.expect('# ')
        self.session.sendline('mount ' + remoteLoc + ':/tftpboot /mnt/nfs') #Mine is at this location
        self.session.expect('# ')
        self.session.sendline('cd /mnt/nfs/bin')
        self.session.expect('# ')
        self.session.sendline('pwd')
        self.session.expect('# ')  

    def RunNexus(self):
        self.session.sendline('killall nxserver')
        self.session.expect('# ')
        print('nx server killed')
        time.sleep(3)
        self.session.sendline('./nexus nxserver &')
        time.sleep(2)
    

    def PlayMovie(self):           
        self.session.sendline(self.Movie)
        print('Play command sent. Please perform Audio and Video tests'+'\n')
        print('You have 2 minutes\n')    
        for t in xrange(120,0,-1):
            minutes = (t / 60)
            seconds = (t % 60)        
            #print('\rPlaying movie [%d:%2d]'%(minutes,seconds)),        
            time.sleep(1.0)             #every second, for 2 minutes
            
    def BreakIn(self):
        self.session.send(chr(3))            #Send a Ctrl+C  
        self.session.sendline('\n')          #Send a CR
        self.session.expect('# ')

    def AllDone(self):
        self.session.sendline('reboot')
        time.sleep(60)
        self.session.sendline('\n')
        self.session.expect('# ')
        print('End of nexus')
    

                                    #print "Running Test... please wait."

                                    #filename = sys.argv[2]
#filename = '0_buycdmn8_0_dpdnx663_2.mp4'
#host = '192.168.1.171'
#host = '192.168.1.174'
#running = 1

                                  #host = sys.argv[1]
#try:
    #session = pxssh.pxssh()
    #command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + host)
    #LogIn(session)
    #RunNexus(session)
    TB1 = TestBox(0,'./nexus.client play ../movies/Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4','Initiated')
    TB1.LogIn()
    TB1.RunNexus()
    TB1.PlayMovie()
    TB1.BreakIn()
    TB1.AllDone()
    
    #print('Play Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4  tile\n')
    #print('Resolution is: 4K\n')
    #cmmnd = ('./nexus.client play ../movies/Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4')
    #PlayMovies(session,cmmnd)
    #print('Play e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4 tile\n')
    #print('Resolution is: 1080p, generic\n')
    #cmmnd = ('./nexus.client play ../movies/e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4')
    #PlayMovies(session,cmmnd)
    #print('Play Inception_TRLR3_720.mp4 tile\n')
    #print('Resolution is: generic 720p\n')
    #cmmnd = ('./nexus.client play ../movies/Inception_TRLR3_720.mp4')
    #PlayMovies(session,cmmnd)
    #print('Play generic 480p clip\n')
    #print('Resolution is: 480p, generic\n')
    #cmmnd = ('./nexus.client play ../movies/0_buycdmn8_0_dpdnx663_2.mp4')
    #PlayMovies(session,cmmnd)    
    #AllDone(session)    
#except:
    #print("Not working")
    #print(session.before)
    #print(session.after)
    

