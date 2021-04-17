import re
import pathlib
import hashlib
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
    TempTxAFile = pathlib.Path("Temp_TxA.txt")
    openTempTxA = open(TempTxAFile, "r")

    transactions = []
    hashedTx = []
    if openTempTxA.mode == 'r':
        index = 0
        for transactionLine in openTempTxA:
            transactions[index] = transactionLine
            index += 1
        hashOper = hashlib.sha256()
        index2 = 0
        for x in range(0,4):
            hashOper.update(transactions[index2].encode("utf-8"))
            hashedTx[index2] = hashOper.hexdigest()
            index2 += 1
    # Use function in instructions to find nonce
    # Combine header and body and store as 116-byte Hex "newBlock"
    # return newBlock
    pass


def processTx(transaction, turn):
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

    # Append Tx to Temp_TxA.txt
    TempTxBFile = pathlib.Path("Temp_TxB.txt")
    openTempTxB = open(TempTxBFile, "a")
    openTempTxB.write(transaction + "\n")
    openTempTxB.close()

    # Check if Tx Payer is client B
    # If true -> send tx to F1
    if transaction[0] == 'B':
        F1Socket.sendto(transaction.encode(), (serverName, connectPortF1))
    else:
        pass


    # Check if number of transactions in Temp_TxB.txt == 4
    blockFull = checkTempTx()
    print("Block full: " + str(blockFull))
    if blockFull:
        turn += 1
        if (turn % 2 == 1):
            print("My turn!")
            #newBlock = mineBlock()
            #processBlock(newBlock)
            return turn
        else:
            return turn
    else:
        pass


def processBlock():
    # Apppend block to blockchain.txt
    # Remove Tx from Temp_B.txt
    # Check Tx and send confirmation to clientB
    # Send block to F1
    # Exit
    pass


def checkTempTx():
    # Checks the Temp_TxB file and returns true if there are 4
    # transactions
    TempTxBFile = pathlib.Path("Temp_TxB.txt")
    openTempTxB = open(TempTxBFile, "r")

    if openTempTxB.mode == 'r':
        lineCount = 0
        for transactionLine in openTempTxB:
            lineCount += 1
        if lineCount == 4:
            return 1
        else:
            return 0
    else:
        pass 


def main():
    turn = 2
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
            newTurn = processTx(incomingMessage, turn)
            if newTurn:
                turn = newTurn
        else:
            pass


if __name__== "__main__":
   main()