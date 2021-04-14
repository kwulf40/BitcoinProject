import re
from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 10000
connectPortClient = 10001
connectPortF2 = 20000
serverSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)
F2Socket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("F1 Operational")

while 1:
    print("F1 Working...")
    message, clientAddress = serverSocket.recvfrom(2048)
    incomingMessage = message.decode()
    clientTxCheck = re.search("Send TX to block.", incomingMessage)
    serverNotifCheck = re.search("TX Notification", incomingMessage)

    if clientTxCheck != None:
        returnMessage = "TX Confirmed."
        serverSocket.sendto(returnMessage.encode(), clientAddress)
        print("Return Message Sent.")
        blockMessage = "TX Notification"
        F2Socket.sendto(blockMessage.encode(), (serverName, connectPortF2))
        print("Other Block Notified")
    elif serverNotifCheck != None:
        print("TX Notification Recieved from Block 2")
    else:
        pass