import re
import pathlib
from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 20001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


#   getClientAccountInfo()
#   reads account names from the balanceA.txt 
#   and returns them as a list
#
def getClientAccountInfo():
    #open balanceB.txt
    clientBFile = pathlib.Path("balanceB.txt")
    if clientBFile.exists():
        activeBalanceB = open(clientBFile, "r")
    else:
        #creates a new initial file if one doesn't exist
        initialBalanceB = open(clientBFile, "w+")
        initialBalanceB.write("B0000001:000003E8:000003E8\n")
        initialBalanceB.write("B0000002:000003E8:000003E8\n")
        initialBalanceB.close()

        activeBalanceB = open(clientBFile, "r")

    #extract user account from each line
    #stores user accounts in a list
    if activeBalanceB.mode == 'r':
        accountNumList = []
        for account in activeBalanceB:

            acctNum = account.split(":")
            accountNumList.append(acctNum[0])
    else:
        print("Error with file")
    
    #return list
    if not accountNumList:
        print ("Error in creating account lists")
        activeBalanceB.close()
        return 0
    else:
        activeBalanceB.close()
        return accountNumList


#   sendClientAccountInfo
#   Function that retrives a client's accounts and sends them over the servers
#   to the other client, to be used in creating a new transaction
#   Sends an array of accounts to the other clients to be used as payees.
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
    # Verify Tx with corresponding TX in Unconfirmed_TxB.txt
    # Reduce Tx amount + Tx fee from account's confirmed balance
    # Removes Tx from Unconfirmed_TxB.txt
    # Appends Tx to Confirmed_TxB.txt
    #
    # If payee:
    # Adds Tx amount to account's confirmed balance.
    # Appends Tx to Confirmed_TxB.txt
    pass


def main():
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()
        
        accountInfoRequest = re.search("Request Client B Accounts", incomingMessage)
        if accountInfoRequest != None:
            accountString = sendClientAccountInfo()
            serverSocket.sendto(accountString.encode(), clientAddress)
            print("Client B Info Sent")
        # on received tx to confirm from block chain,
        # call verifyTX(transactionArray)
        else:
            pass


if __name__== "__main__":
   main()