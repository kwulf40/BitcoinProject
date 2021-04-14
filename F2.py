import re
from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 20000
connectPortClient = 20001
connectPortF1 = 10000
serverSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)
F1Socket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("F2 Operational")

while 1:
    print("F2 Working...")
    message, clientAddress = serverSocket.recvfrom(2048)
    incomingMessage = message.decode()
    clientTxCheck = re.search("Send TX to block.", incomingMessage)
    serverNotifCheck = re.search("TX Notification", incomingMessage)

    if clientTxCheck != None:
        returnMessage = "TX Confirmed."
        serverSocket.sendto(returnMessage.encode(), clientAddress)
        print("Return Message Sent.")
        blockMessage = "TX Notification"
        F1Socket.sendto(blockMessage.encode(), (serverName, connectPortF1))
        print("Other Block Notified")
    elif serverNotifCheck != None:
        print("TX Notification Recieved from Block 1")
    else:
        pass