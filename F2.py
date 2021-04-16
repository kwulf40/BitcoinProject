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


def requestAccountsF1():
    requestMessage = "Request Client A Accounts"
    F1Socket.sendto(requestMessage.encode(), (serverName, connectPortF1))
    acctString, serverAddress = F1Socket.recvfrom(2048)
    return acctString


def requestClientAccounts():
    requestMessage = "Request Client B Accounts"
    clientSocket.sendto(requestMessage.encode(), (serverName, connectPortClient))
    acctString, serverAddress = clientSocket.recvfrom(2048)
    return acctString


def mineBlock():
    # Hash header of last block and store in lastBlockHash
    # Create Merkle root from 4 Temp_B.txt tx
    # Use function in instructions to find nonce
    # Combine header and body and store as 116-byte Hex "newBlock"
    # return newBlock
    pass


def processTX():
    # Append Tx to Temp_B.txt
    # Check if Tx Payer is client B
    # If true -> send tx to F1
    #
    # Check if number of transactions in Temp_B.txt == 4
    # If yes, turn++
    #
    # If the server's turn value is odd, exit the function
    # Else 
    #   newBlock = mineBlock()
    #   Add mining fee and total Tx fee to node's account balanceF2.txt
    #   Apppend block to blockchain.txt
    #   Check Tx and send confirmation to clientB
    #   Send block to other server
    #   Print the new block
    #   Exit
    pass


def processBlock():
    # Apppend block to blockchain.txt
    # Remove Tx from Temp_B.txt
    # Check Tx and send confirmation to clientB
    # Exit
    pass


def main():
    while 1:
        print("F2 Working...")
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()

        #
        # regex function calls to identify the incoming message.
        #
        # transationCheck will be true if the first 8 digits of the incoming message are 
        # in the format of a client account, signaling an incoming transactions
        #
        # serverRequest will be true if the message is a request from Client B for the F1 client A accounts
        #
        # localRequest will be true if the message is a request from F1 for the local Client B accounts 
        transactionCheck = re.match(r'([A-B])([0]{6})([1-2])', incomingMessage)
        serverRequest = re.search("Request F1 Accounts", incomingMessage)
        localRequest = re.search("Request Client B Accounts", incomingMessage)

        #if-elif to check the true-false value of each message checks
        #if serverRequest is true, get client A accounts from F1 and send to client B
        if serverRequest:
            print("Requesting Clients From F1")
            acctString = requestAccountsF1()
            print("Sending Accounts to Client B")
            serverSocket.sendto(acctString, clientAddress)
        #if localRequest is true, get client B accounts from local and send to F1
        elif localRequest:
            print("Getting accounts from Client B")
            acctString = requestClientAccounts()
            print("Sending accounts to F1")
            serverSocket.sendto(acctString, clientAddress)
        #if transactionCheck is true, the message is tx information to be stored in temp_TxB.txt    
        elif transactionCheck:
            print("Received Tx!")
            print(incomingMessage)
        else:
            pass


if __name__== "__main__":
   main()