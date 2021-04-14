from socket import *
serverName = 'localhost'
serverPort = 20000
connectPortClient = 20001
connectPortF1 = 10000
serverSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)
F1Socket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('', serverPort))