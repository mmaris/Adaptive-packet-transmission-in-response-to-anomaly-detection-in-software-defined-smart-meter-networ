from socket import *
import time
from threading import *
grace = 0.1
previous = -1
iarr = 0.0
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
            current = time.time()
            if previous == -1:
                previous = current
            else:
                iarr = current - previous - grace
                previous = current
            print("Iarr time is %f"%iarr)
            #start thread to process stuff

            
except Exception as e:
    print(str(e))
finally:
    connectionSocket.close()
    serverSocket.close()
