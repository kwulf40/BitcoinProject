import re
import pathlib
import hashlib
import fileinput
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


def createBalance():
    balanceF1File = pathlib.Path("balanceF1.txt")
    initialBalanceF1 = open(balanceF1File, "w+")
    initialBalanceF1.write("F1000001:00000000\n")
    initialBalanceF1.close()


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
    hashOper = hashlib.sha256()

    # Hash header of last block and store in lastBlockHash
    blockchain = pathlib.Path("BlockchainA.txt")
    if blockchain.exists():
        openBlockchain = open(blockchain, "r")
        for block in reversed(list(openBlockchain)):
            lastHeader = str(block)[:137]
            hashOper.update(lastHeader.encode("utf-8"))
            lastBlockHash = hashOper.hexdigest()
    else: 
        lastBlockHash = '0000000000000000000000000000000000000000000000000000000000000000'

    # Create Merkle root from 4 Temp_TxA.txt 
    TempTxAFile = pathlib.Path("Temp_TxA.txt")
    openTempTxA = open(TempTxAFile, "r")

    transactions = []
    hashedTx = []
    if openTempTxA.mode == 'r':
        for transactionLine in openTempTxA:
            transactions.append(transactionLine)
        index = 0
        for x in range(0,4):
            hashOper.update(transactions[index].encode("utf-8"))
            hashedTx.append(hashOper.hexdigest())
            index += 1
        hashOper.update((hashedTx[0] + hashedTx[1]).encode("utf-8"))
        hashAB = hashOper.hexdigest()
        hashOper.update((hashedTx[2] + hashedTx[3]).encode("utf-8"))
        hashCD = hashOper.hexdigest()
        hashOper.update((hashAB + hashCD).encode("utf-8"))
        merkleRoot = hashOper.hexdigest()
        print("Merkle: " + merkleRoot)
    else:
        print("Error opening temp for mining")
        return 0
    openTempTxA.close()

    #   Use function in instructions to find nonce
    nonce = 0 
    while True: 
        block_header = str(nonce).zfill(8) + lastBlockHash + merkleRoot
        hashOper.update(block_header.encode("utf-8")) 
        hashValue = hashOper.hexdigest() 
        #print('nonce:{0}, hash:{1}'.format(nonce, hashValue)) 
        nounceFound = True 
        for i in range(4): 
            if hashValue[i]!='0': 
                nounceFound = False 
        if nounceFound: 
            break 
        else: nonce = nonce + 1

    # Combine header and body and store as 116-byte Hex "newBlock"
    newBlock = block_header + transactions[0].rstrip('\n') + transactions[1].rstrip('\n') + transactions[2].rstrip('\n') + transactions[3].rstrip('\n')
    return newBlock


def addFees():
    fees = 38
    modifiedFlag = 0
    modifiedBalance = "balanceF1.txt"
    with fileinput.FileInput(modifiedBalance, inplace=True) as file:
        for line in file:
            tempAcctInfo = str(line)
            acctVar = line.split(":")
            if acctVar[0] == "F1000001":
                newAcctVar = []
                balance = int(acctVar[1], 16)
                newBal = balance + fees
                newAcctVar.append(acctVar[0])
                newAcctVar.append(str('%08X' % newBal))
                newAcctInfo = (newAcctVar[0] + ":" + newAcctVar[1])
                print(line.replace(tempAcctInfo, newAcctInfo), end='')
                modifiedFlag = 1
            else:
                print(line, end='')
    file.close()
    print("Awarded account: " + newAcctVar[0] + " with fees for new balance of: " + str(newBal))
    if modifiedFlag:
        return 1
    else:
        return 0


def processTx(transaction, turn):
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
    #   Send block to other server
    #   Check Tx and send confirmation to clientA
    #   Print the new block
    #   Exit

    # Append Tx to Temp_TxA.txt
    TempTxAFile = pathlib.Path("Temp_TxA.txt")
    openTempTxA = open(TempTxAFile, "a")
    openTempTxA.write(transaction + "\n")
    openTempTxA.close()

    # Check if Tx Payer is client A
    # If true -> send tx to F2
    if transaction[0] == 'A':
        F2Socket.sendto(transaction.encode(), (serverName, connectPortF2))
    else:
        pass


    # Check if number of transactions in Temp_TxA.txt == 4
    blockFull = checkTempTx()
    print("Block full: " + str(blockFull))
    if blockFull:
        turn += 1
        if (turn % 2 == 1):
            print("My turn!")
            newBlock = mineBlock()
            print("Block from F1: " + newBlock)
            #   Send block to other server
            F2Socket.sendto(newBlock.encode(), (serverName, connectPortF2))
            #   Add mining fee and total Tx fee to node's account balanceF1.txt
            addFees()
            #   Apppend block to blockchain.txt
            processBlock(newBlock)
            return turn
        else:
            return turn
    else:
        pass


def processBlock(block):
    # Apppend block to blockchain.txt
    blockchainFile = pathlib.Path("BlockchainA.txt")
    openBlockchainA = open(blockchainFile, "a")
    openBlockchainA.write(block + "\n")
    openBlockchainA.close()

    # Remove Tx from Temp_TxA.txt  
    print("Clearing Temp_TxA")
    TempTxAFile = pathlib.Path("Temp_TxA.txt")
    modifiedTempTxA = open(TempTxAFile, "w+")
    modifiedTempTxA.close()

    # Check Tx and send confirmation to clientA
    blockTxBody = str(block)[136:]
    print("Tx body: " + blockTxBody)
    txInfo = []
    n = 24
    #store each tx in the block body
    for index in range(0, len(blockTxBody), n):
        txInfo.append(blockTxBody[index : index + n])
    #for each tx, check for client account in the tx
    #if client account found, send the tx to the client for confirmation
    for tx in txInfo:
        stringTx = str(tx)
        print("Tx: " + stringTx)
        if stringTx[0] == 'A' or stringTx[8] == 'A':
            txMessage = stringTx
            print("Sending tx for confirmation " + stringTx)
            clientSocket.sendto(txMessage.encode(), (serverName, connectPortClient))


def checkTempTx():
    # Checks the Temp_TxA file and returns true if there are 4
    # transactions
    TempTxAFile = pathlib.Path("Temp_TxA.txt")
    openTempTxA = open(TempTxAFile, "r")

    if openTempTxA.mode == 'r':
        lineCount = 0
        for transactionLine in openTempTxA:
            lineCount += 1
        if lineCount == 4:
            return 1
        else:
            return 0
    else:
        pass 


def main():
    createBalance()
    turn = 2
    while 1:
        print("F1 Working...")
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
        transactionCheck = re.match(r'(^([A-B])([0]{6})([1-2]))', incomingMessage)
        if len(incomingMessage) > 200: 
            blockCheck = True
        else:
            blockCheck = False
        serverRequest = re.search("Request F2 Accounts", incomingMessage)
        localRequest = re.search("Request Client A Accounts", incomingMessage)

        #if-elif to check the true-false value of each message checks
        #if serverRequest is true, get client B accounts from F2 and send to client A
        if serverRequest:
            print("Requesting Clients From F2")
            acctString = requestAccountsF2()
            print("Sending Accounts to Client A")
            serverSocket.sendto(acctString, clientAddress)
        #if localRequest is true, get client A accounts from local and send to F2
        elif localRequest:
            print("Getting accounts from Client A")
            acctString = requestClientAccounts()
            print("Sending accounts to F2")
            serverSocket.sendto(acctString, clientAddress)
        #if transactionCheck is true, the message is tx information to be stored in temp_TxA.txt 
        elif transactionCheck:
            print("Received Tx!")
            newTurn = processTx(incomingMessage, turn)
            if newTurn:
                turn = newTurn
        elif blockCheck:
            print("Recieved Block!")
            processBlock(incomingMessage)
        else:
            pass


if __name__== "__main__":
   main()