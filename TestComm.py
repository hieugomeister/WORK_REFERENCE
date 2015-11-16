'''
#--------------------------------------------------------------------------------------------------
#For wireless, it is possible to execute wificonnect.sh
#remotely to enable WLAN0 IpAddress
#
#
#       The Play3 class requires the following values:
#       Channel type:
#       0 = Wireless LAN
#       1 = RJ45 Ethernet
#       2 = MoCA
#       The Laptop IP address
#       The STB IP address
#       The movie title
#       02/25/2015  -  Hieu Pham        
#---------------------------------------------------------------------------------------------------
'''

#!/usr/bin/env python

import os
import re
import sys
import time
import Play3
import string
import CommPort
import subprocess
import netifaces as ni

bigString = ''

def ConnectToSTB(hwdev):
    cs = CommPort.CommSerial(hwdev,115200,8,'N',1,3,3)
    cs.InitPort()
    cs.CommOpen()
    cs.CheckPortStatus()
    cs.WritePort('\n')
    time.sleep(1)
    cs.WritePort('reboot')
    print(cs)           #Print out the object
    time.sleep(55)      #Wait for STB boot sequence to complete

    #-----------------------------------------------------------------
    #Was trying to use subprocess.check_call() to examine laptop IP,
    #but there was a better way
    #subprocess.check_call("ifconfig > /home/oncue/Downloads/Working/
    #                                  laptopip.txt",shell=True)
    #-----------------------------------------------------------------

    ni.ifaddresses('eth0')
    ipLT = ni.ifaddresses('eth0')[2][0]['addr']
    print("Laptop IP Address: " + ipLT)  # should print "xxx.xxx.xxx.xxx" now
    cs.WritePort('\n') #Do so to force a prompt
    mountstring = "mount " + ipLT + ":/tftpboot /mnt/nfs"
    print("Sending serial command... " + mountstring)
    cs.WritePort(mountstring)
    time.sleep(1)
    cs.WritePort('\n')
    rxb = cs.ReadPort(3)
    if(rxb[2] == '#'):
        print("STB prompt = " + rxb[2] + " STB mounted to " + ipLT + ":/tftpboot - Status: Success")
    else:
        print("STB prompt = " + rxb[2] + " STB mounted to " + ipLT + ":/tftpboot - Status: Failed")
    cs.FlushPort(0)
    time.sleep(0.5)
    cs.FlushPort(1)
    time.sleep(0.5)
    cs.WritePort("ifconfig")
    bigString = cs.ReadPort(1250)    
    spos = bigString.find('inet addr:')     #Position of inet address:
    spos2 = bigString.find('Bcast:')        #Position of Bcast:
    stbIP = bigString[(spos+10):(spos2-1)]  #Our ip is right in between
    print(stbIP)
    return(ipLT,stbIP)    
    #-------------------------------------------------------------------------

(LapTopMachine, STBMac) = ConnectToSTB('/dev/ttyUSB0')


TB1 = Play3.TestBox(1,LapTopMachine,STBMac,'./nexus.client play ../movies/Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4')
TB1.LogIn()
TB1.RunNexus()
TB1.PlayMovie()
TB1.BreakIn()
TB1.AllDone()
print("Movie played: " + "Bosphorus_3840x2160_120fps_420_8bit_HEVC_MP4.mp4")
print("Status: " + TB1.status)

if TB1.Ichannel == 0:
    time.sleep(110) #Give it about 2 minutes to finish setting up WLAN0

print(TB1)

TB2=Play3.TestBox(1,LapTopMachine,STBMac,'./nexus.client play ../movies/e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4') 
TB2.LogIn()
TB2.RunNexus()
TB2.PlayMovie()
TB2.BreakIn()
TB2.AllDone()
print("Movie played: " + "e4a3dc-hlf00849_pswr_7-the_force-awakens-official-teaser-h264h_aac_1920x1080_7840x160.mp4")
print("Status: " + TB2.status)

if TB2.Ichannel == 0:
    time.sleep(110) #Give it about 2 minutes to finish setting up WLAN0
    
print(TB2)

TB3=Play3.TestBox(1,LapTopMachine,STBMac,'./nexus.client play ../movies/Inception_TRLR3_720.mp4') 
TB3.LogIn()
TB3.RunNexus()
TB3.PlayMovie()
TB3.BreakIn()
TB3.AllDone()
print("Movie played: " + "./nexus.client play ../movies/Inception_TRLR3_720.mp4")
print("Status: " + TB3.status)

if TB3.Ichannel == 0:
    time.sleep(110) #Give it about 2 minutes to finish setting up WLAN0
    
print(TB3)

TB4=Play3.TestBox(1,LapTopMachine,STBMac,'./nexus.client play ../movies/0_buycdmn8_0_dpdnx663_2.mp4')            
TB4.LogIn()
TB4.RunNexus()
TB4.PlayMovie()
TB4.BreakIn()
TB4.AllDone()
print("Movie played: " + "./nexus.client play ../movies/0_buycdmn8_0_dpdnx663_2.mp4")
print("Status: " + TB4.status)

if TB4.Ichannel == 0:
    time.sleep(110) #Give it about 2 minutes to finish setting up WLAN0

print(TB4)
