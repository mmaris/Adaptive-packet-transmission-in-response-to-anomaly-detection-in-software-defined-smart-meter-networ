from socket import *
import time
from threading import *

resultsFile = open("ServerDynamicData.txt", "w")

alpha = 0.1
grace = 1
previousTime = 0.0
iarrTime = -1.0

class SendResponse(Thread):
    def __init__(self, currentTime, message):
        self.currentTime = currentTime
        self.message =  message
        Thread.__init__(self)
        self.start()

    def run(self):
        global grace
        #send back the interarrivl time
        try:
            grace = float(self.message.split(',')[1])
            packNum = int(self.message.split(',')[2])
            print("grace is %f and %i"%(grace,packNum))
            connectionSocket.send(("%.9f "%self.getTime()).encode())
        except Exception as e:
            print(str(e))


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

        resultsFile.write("%f.9\n"%iarrTime)
        previousTime = currentTime
        return iarrTime


#*******
# main:

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

connectionSocket, clientAddress = serverSocket.accept()

try:
    print("i'm here")
    with open("Received_Measurements.txt","w") as outfile:
        while 1:
            # await the next message
            message = connectionSocket.recv(2048).decode()
            # handle empty message, usually a cause of dropping connection client side.
            if message == '':
                print('Empty message received. Closing socket.')
                break

            #print("received: %s" % message)

            # make this a thread
            # get interarrival time
            currentTime = time.time()

            # start a thread to send the interarrival time
            SendResponse(currentTime, message)

            #start thread to process stuff

            
except Exception as e:
    print(str(e))
finally:
    connectionSocket.close()
    serverSocket.close()
