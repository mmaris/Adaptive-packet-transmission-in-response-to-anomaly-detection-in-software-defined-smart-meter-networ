from socket import *
from time import time, sleep
from threading import *

resultsFile = open("UDPLoggingFile.txt", "w")

serverIP = '127.0.0.1'
serverPort = 12001
serverAddr = (serverPort, serverAddr)
clientIP = '127.0.0.1'
ckuebtPort = 12002
clientAddr = (clientPort, clientAddr)

def SendAck(Thread):
    def __init__(self, currentTime, message):
        self.currentTime = currentTime
        self.message =  message
        Thread.__init__(self)
        self.start()

    def run(self):
        global clientAddr
        #send back the interarrivl time
        

    def getTime(self):
        global resultsFile
        global iarrTime
        global alpha
        global grace
        global previousTime
        #print("current is: %.9f , and previous is: %.9f"% (self.currentTime, previousTime))

        if iarrTime > 0:
            iarrTime = alpha * (self.currentTime - previousTime - grace) + (1-alpha) * iarrTime
        elif iarrTime == 0:
            iarrTime = self.currentTime - previousTime - grace
        else:
            iarrTime = 0

        print("calculated iarrTime as %f"%iarrTime)
        #resultsFile.write("%f.9,%i\n"%iarrTime,self.packNum)
        previousTime = currentTime
        return iarrTime


    try:
        self.grace = float(self.message.split(',')[1])
        self.packNum = int(self.message.split(',')[2])
        print("grace is %f and %i"%(grace,self.packNum))
        serverSocket.sendto(("%.9f,%i "%(self.getTime(),self.packNum)).encode(), ClientAddr)
    except Exception as e:
        print(str(e))
