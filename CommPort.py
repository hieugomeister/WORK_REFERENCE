'''
*   This is the serial port class
*   Methods are:
*       InitPort
*       CommOpen
*       CommClose
*       CheckPortStatus
*       WritePort
*       ReadPort
*       FlushPort
*
*       02/25/2015 - Hieu Pham
'''
import serial
import time
import sys

class CommSerial:
    commName        =   ''
    baudRate        =   1200
    byteSize        =   4
    parityBit       =   ''
    stopBit         =   0
    timeOut         =   None
    writeTimeout    =   None
    initstatus      =   'High-Z'
    commopenstate   =   False
    commclosestate  =   True
    TXMessage       =   ''
    RXBuffer        =   ''
    def __init__ (self,pn,br,bs,pb,sb,to,wto):
        self.commName       =   pn
        self.baudRate       =   br
        self.byteSize       =   bs
        self.parityBit      =   pb
        self.stopBit        =   sb
        self.timeOut        =   to
        self.writeTimeout   =   wto
    def InitPort(self):
        self.serieau = serial.Serial(self.commName, self.baudRate, self.byteSize, self.parityBit, self.stopBit, self.timeOut, self.writeTimeout)
        self.initstatus = 'Initialized'
        return(self.initstatus)
    def CommOpen(self):
        self.serieau.close()
        time.sleep(1)
        self.serieau.open()
        self.commopenstate = self.serieau.isOpen()
        return(self.commopenstate)
    def ComClose(self):
        self.serieau.close()
        self.commclosestate = self.serieau.isOpen()
        return(self.commclosestate)
    def CheckPortStatus(self):
        return(self.commopenstate)
    def WritePort(self,messageString):
        self.TXMessage = messageString
        self.serieau.write(self.TXMessage + '\x0D' + '\x0A')
        print("Wrote " + self.TXMessage + "\n")
    def ReadPort(self, NoB):
        self.RXBuffer = self.serieau.read(NoB)
        return(self.RXBuffer)
    def FlushPort(self, devReg):
        if(devReg == 0): #0 = input
            self.serieau.flushInput()
        else: #1 = output
            self.serieau.flushOutput()        
    def __str__(self):
        return("Comm port is: " + self.commName + "\n"
               + "Baud Rate is: " + str(self.baudRate) + "\n"
               + "Data bits = " + str(self.byteSize) + "\n"
               + "Stop bits = " + str(self.stopBit) + "\n"
               + "Paraity = " + self.parityBit + "\n"
               + "Time out = " +  str(self.timeOut) + "\n"
               + "Write time out = " + str(self.writeTimeout) + "\n"
               + "Port status: " + str(self.commopenstate) + "\n")
    
        
        
