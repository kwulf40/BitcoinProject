import re
import pathlib
from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 10001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


#   getClientAccountInfo()
#   reads account names from the balanceA.txt 
#   and returns them as a list
#
def getClientAccountInfo():
    #open balanceA.txt
    clientAFile = pathlib.Path("balanceA.txt")
    if clientAFile.exists():
        activeBalanceA = open(clientAFile, "r")
    else:
        #creates a new initial file if one doesn't exist
        initialBalanceA = open(clientAFile, "w+")
        initialBalanceA.write("A0000001:000003E8:000003E8\n")
        initialBalanceA.write("A0000002:000003E8:000003E8\n")
        initialBalanceA.close()

        activeBalanceA = open(clientAFile, "r")

    #extract user account from each line
    #stores user accounts in a list
    if activeBalanceA.mode == 'r':
        accountNumList = []
        for account in activeBalanceA:

            acctNum = account.split(":")
            accountNumList.append(acctNum[0])
    else:
        print("Error with file")
    
    #returns list
    if not accountNumList:
        print ("Error in creating account lists")
        activeBalanceA.close()
        return 0
    else:
        activeBalanceA.close()
        return accountNumList


#   sendClientAccountInfo
#   Function that retrives a client's accounts and sends them over the servers
#   to the other client, to be used in creating a new transaction
#   Sends a list of accounts to the other clients to be used as payees.
#
def sendClientAccountInfo():
    #call getClientAccountInfo
    message = getClientAccountInfo()
    messageString = ":".join(message)
    #return the Account names as a string
    return messageString


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
        
        accountInfoRequest = re.search("Request Client A Accounts", incomingMessage)
        if accountInfoRequest != None:
            accountString = sendClientAccountInfo()
            serverSocket.sendto(accountString.encode(), clientAddress)
            print("Client A Info Sent")
        # on received tx to confirm from block chain,
        # call verifyTX(transactionArray)
        else:
            pass


if __name__== "__main__":
   main()