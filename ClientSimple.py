from socket import *
from threading import *
import time
from random import *
from math import floor

#alpha = 0.1
#sendingTime = 0.0

MTU = 1400
N = MTU
n = 0.1
packetsOut = 0
            
class SendData(Thread):
    def __init__(self, data, N):
        self.data = data
        self.N = N
        Thread.__init__(self)
        self.start()
        
    def run(self):
        global packetsOut        
        grace = n
        
        clientSocket.send((self.data+",%f"%grace).encode())
        

#********
# main:

serverName = '127.0.0.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)

try:

    clientSocket.connect((serverName, serverPort))
    
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
