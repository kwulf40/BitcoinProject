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


def requestAccountsF2():
    requestMessage = "Request Client B Accounts"
    F2Socket.sendto(requestMessage.encode(), (serverName, connectPortF2))
    acctString, serverAddress = F2Socket.recvfrom(2048)
    return acctString


def requestClientAccounts():
    requestMessage = "Request Client A Accounts"
    clientSocket.sendto(requestMessage.encode(), (serverName, connectPortClient))
    acctString, serverAddress = clientSocket.recvfrom(2048)
    return acctString


def mineBlock():
    # Hash header of last block and store in lastBlockHash
    # Create Merkle root from 4 Temp_TxA.txt 
    # Use function in instructions to find nonce
    # Combine header and body and store as 116-byte Hex "newBlock"
    # return newBlock
    pass


def processTX():
    # Append Tx to Temp_TxA.txt
    # Check if Tx Payer is client A
    # If true -> send tx to F2
    #
    # Check if number of transactions in Temp_TxA.txt == 4
    # If yes, turn++
    #
    # If the server's turn value is odd, exit the function
    # Else 
    #   newBlock = mineBlock()
    #   Add mining fee and total Tx fee to node's account balanceF1.txt
    #   Apppend block to blockchain.txt
    #   Check Tx and send confirmation to clientA
    #   Send block to other server
    #   Print the new block
    #   Exit
    pass


def processBlock():
    # Apppend block to blockchain.txt
    # Remove Tx from Temp_TxA.txt
    # Check Tx and send confirmation to clientA
    # Exit
    pass


def main():
    while 1:
        print("F1 Working...")
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()

        #
        # Check if the message is a transaction or a block (format)
        # 
        # If transaction, call processTX()
        # If else is block, call processBlock()

        serverRequest = re.search("Request F2 Accounts", incomingMessage)
        localRequest = re.search("Request Client A Accounts", incomingMessage)
        if serverRequest != None:
            print("Requesting Clients From F2")
            acctString = requestAccountsF2()
            print("Sending Accounts to Client A")
            serverSocket.sendto(acctString, clientAddress)
        elif localRequest != None:
            print("Getting accounts from Client A")
            acctString = requestClientAccounts()
            print("Sending accounts to F2")
            serverSocket.sendto(acctString, clientAddress)
        else:
            pass


if __name__== "__main__":
   main()