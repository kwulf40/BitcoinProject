from socket import *
serverName = 'localhost'
serverPort = 10000
connectPortClient = 10001
connectPortF2 = 20000
serverSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)
F2Socket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('', serverPort))