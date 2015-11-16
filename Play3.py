import os
import re
import sys
import time
import pexpect
import logging
import getpass
import traceback
import subprocess

MiscCmd = 'wificonnect.sh FiOS-OD9CD 5946rescue9135tip'
hostWC = '192.168.1.172'
hostWL = '192.168.1.174'
remoteLoc = '192.168.1.176'

#------------------------Class Definition-----------------------------------------------------------
class TestBox:
    GarbStr = ''
    ProcStat = False
    ProcStat1 = False
    ProcStat2 = False
    search1 = -1
    search2 = -1
    status = 'Not_Tested'
    IPAddress = ''
    STB_IPAddress = ''
    command = ''
    def __init__(self,InetChannel,ipaddress,ipaddress2,MovieToPlay):
        self.Ichannel = InetChannel
        self.Movie = MovieToPlay
        self.Error = 'Instantiated'
        self.IPAddress = ipaddress
        self.STB_IPAddress = ipaddress2
        self.SetSession() #Set the session based on channel type        
        print(self.Error)
    def SetSession(self):
        if self.Ichannel == 0: #WLAN
            self.command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + self.STB_IPAddress)            
        elif self.Ichannel == 1 or self.Ichannel == 2: #RJ45 or MoCA            
            self.command = ('ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@' + self.STB_IPAddress)            
    def die(self):
        self.Error = 'Connection problem...'
        print(self.Error)
        print(self.session.before, self.session.after)
        self.session.terminate()
        exit(1)
    def LogIn(self):
        self.session = pexpect.spawn(self.command)
        self.session.expect('password: ') #Now session is created                   
        self.session.sendline('verizon123')
        self.session.expect_exact('# ')
        self.session.sendline('su -')
        self.session.expect('# ')
        self.session.sendline('cd ..')
        self.session.expect('# ')
        self.session.sendline('mount ' + self.IPAddress + ':/tftpboot /mnt/nfs') #Mine is at this location
        self.session.expect('# ')
        self.session.sendline('cd /mnt/nfs/bin')
        self.session.expect('# ')
        self.session.sendline('pwd')
        self.session.expect('# ')
        self.Error = 'Logged In'
        print(self.Error)
    def RunNexus(self):
        self.session.sendline('killall nxserver')
        self.session.expect('# ')
        print('nx server killed')
        time.sleep(3)
        self.session.sendline('./nexus nxserver &')
        time.sleep(2)
        self.session.sendline('\n')
        self.session.expect('# ')
    def PlayMovie(self):  #Calls GetPrompt() and ProcessString()         
        self.session.sendline(self.Movie)
        print('Play command sent. Please perform Audio and Video tests'+'\n')
        print('You have 2 minutes\n')
        self.session.send('ls nexus') #Fetch a file name nexus for details.
        self.session.sendline('\n')
        time.sleep(2) #Give it some static delay
        self.GetPrompt('initialized')
        print("First get..." + "\n")
        print(self.GarbStr)
        self.GetPrompt('server listening')
        print("Second get..." + "\n")
        print(self.GarbStr)
        #self.ProcessString()
        time.sleep(100)
        if self.search1 == 1 and self.search2 == 1:
            self.status = 'PASSED'
        else:
            self.status = 'FAILED'
    def BreakIn(self):
        self.session.send(chr(3))            #Send a Ctrl+C  
        self.session.sendline('\n')          #Send a CR
        self.session.expect('# ')
    def GetPrompt(self,inputstr):
        searchstat=self.session.expect(inputstr)
        self.GarbStr = self.session.before #Bring in this garbage string for post-processing
        if searchstat == 0:
            self.search1 += 1
        else:
            self.search1 -= 1

        if self.search1 == 1:
            self.search2 = 1
        else:
            self.search2 = -1        
        
    def ProcessString(self):
        garbage=''
        mperr = False
        self.ProcStat=re.search("(unable to play)", self.GarbStr)
        if self.ProcStat:
            print(self.GarbStr)
            print("\nVideo Playback FAILED\n")
        else:
            self.ProcStat1=re.search("(discarding unknown sample)", self.GarbStr)
            if self.ProcStat1:
                print(self.GarbStr)
                print("Error: Unsupported 4K H264 video detected")
                print("\nVideo Playback FAILED\n")
            else:
                for t in xrange(120,0,-1):
                    minutes = (t / 60)
                    seconds = (t % 60) #print('\rPlaying movie [%d:%2d]'%(minutes,seconds)),        
                    time.sleep(1.0) #every second, for 2 minutes

                self.session.sendline('\x03')
        self.session.prompt()
        garbage=self.session.before
        print(garbage)
        self.ProcStat2=re.search("(MP4 )", garbage)
        if self.ProcStat2:
            print("Detected Media Format: ", self.ProcStat2.group(1))
            mperr = re.search("(ERR)", garbage)
            if mperr:
                print("\nVideo Playback FAILED\n")
            else:
                            print("\nVideo Playback PASSED\n")
        else:
                    print("\nVideo Playback FAILED\n")            
    def AllDone(self):
        self.session.sendline('sync')
        self.session.sendline('reboot')
        time.sleep(55)
        self.session.sendline('\n')
        self.session.expect('# ')
        print('End of nexus')
        if self.Ichannel == 0: #WLAN
            self.host = hostWL            
            print('Please perform the wificonnect.sh procedure to re-establish ip address' + '\n')
            print('Command is: ' + 'wificonnect.sh FiOS-OD9CD 5946rescue9135tip' + '\n')
            #self.session = pexpect.spawn(self.command)
        elif self.Ichannel == 1 or self.Ichannel == 2: #RJ45 or MoCA
            self.host = hostWC
    def __str__(self):
        return("Laptop IP Address: " + self.IPAddress + "\n"
               + "Set Top Box IP Address: " + self.STB_IPAddress + "\n")
#------------------------Class Definition----------------------------------------------------------- 
