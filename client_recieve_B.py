from socket import *
serverName = 'localhost'
serverPort = 20001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))