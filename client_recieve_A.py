from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 10001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


def verifyTX(transactionArray):
    #
    # for each item in array, check if clientB is payer or payee:
    # 
    # If payer:
    # Verify Tx with corresponding TX in Unconfirmed_TxA.txt
    # Reduce Tx amount + Tx fee from account's confirmed balance
    # Removes Tx from Unconfirmed_TxA.txt
    # Appends Tx to Confirmed_TxA.txt
    #
    # If payee:
    # Adds Tx amount to account's confirmed balance.
    # Appends Tx to Confirmed_TxA.txt
    pass


def main():
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()
        
        # on received tx to confirm from block chain,
        # call verifyTX(transactionArray)
        pass


if __name__== "__main__":
   main()