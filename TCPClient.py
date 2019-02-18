from socket import *
from threading import *
import time
from random import *
from math import floor

#alpha = 0.1
#sendingTime = 0.0

MTU = 1400
N = MTU
NMutex = Lock()
n = 0.001
packetsOut = 0

class GetN(Thread):
    def __init__(self, message):
        self.message = message
        Thread.__init__(self)
        self.start()        

    def run(self):
        global N
        global MTU
        global packetsOut

        for chunk in self.message.split():
            print ("*****",chunk)
            # decrement the packets that are out since we just received the response
            packetsOut -= 1
            #print("Interarrival time is: ",self.message,'\n------\n')
            iarrTime = float(chunk)
            
            if iarrTime <= 0:
                N = MTU
            else:
                N = floor(min(MTU*3,MTU*(0.003/iarrTime - packetsOut)))
            print("Max N is: %i and packets out is %i"%(N,packetsOut))

            
class SendData(Thread):
    def __init__(self, data, N):
        self.data = data
        self.N = N
        Thread.__init__(self)
        self.start()
        
    def run(self):
        global packetsOut        
        grace = n
        
        while self.N > 0:
            if self.N <= MTU:
                clientSocket.send((self.data+",%f"%grace).encode())
                packetsOut += 1
                #print("sending last packet")
                break
            else:
                clientSocket.send((self.data[:MTU]+",%f"%grace).encode())
                self.N -= MTU
                self.data = self.data[MTU:]
                #print("snding intermediate packet")
                packetsOut += 1
                grace = n/5
                time.sleep(n/5)
        
class ReceiveIarrTime(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        while(1):
            message = clientSocket.recv(1024).decode()
            GetN(message)


#********
# main:

serverName = '127.0.0.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)

try:

    clientSocket.connect((serverName, serverPort))
    ReceiveIarrTime()
    
    while 1:
        #sendingTime = time.time()
        #data = str(line[:-1]) + "," + "%.9f" % n
        
        a = []
        for i in range(N): a += str(randint(0,9))
        data = ''.join(a)
        
        SendData(data, N)
        
        # to simulate sending data to the monitoring center every n seconds
        time.sleep(n) 

except Exception as e:
    print(e)

finally:
    clientSocket.close()
