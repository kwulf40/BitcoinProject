import pathlib
from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 10000
clientSocket = socket(AF_INET, SOCK_DGRAM)


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

            print(account)
            acctNum = account.split(":")
            accountNumList.append(acctNum[0])
            print("Read in from file test: " + acctNum[0] + "\n")
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
#   Sends an array of accounts to the other clients to be used as payees.
#
def sendClientAccountInfo():
    #call getClientAccountInfo
    #send array to F1 server
    pass


def newTransaction():
        #=========================================
    #   To create a new Tx:
    #
    #   call getClientAccountInfo
    #   List to user and they select an account as payer
    #
    #   Send a server message to F1 to get clientB accounts through F2
    #   List retrieved account names to user to select as payee
    #
    #   User enters transaction amount
    #   Check if user entered amount + fee is more than payer account(unconfirmed balance)
    #   If true, break
    #   If not true, subtract amount + fee from unconfirmed balance
    #
    #   Store Tx information in variable as 12-byte hex
    #   Append tx to Unconfirmed_TxA.txt
    #   Send tx to F1 node

    print("Getting Account Numbers\n")
    accounts = getClientAccountInfo()
    for ID in accounts:
        print("Account Number: " + ID + "\n")



def currentBalance():
    #Get account info from balance.txt
    #loop for each account
    #Print account name
    #print unconfirmed balance
    #print confirmed balance
    pass


def unconfirmedTX():
    #open Unconfirmed_T.txt
    #print each line
    pass


def confirmedTX(numOfTX):
    #open Confirmed_T.txt
    #print the numOfTX lines of confirmed transactions
    pass


def printBlockchain():
    #Extra Credit
    #Retrieve blockchain.txt info from controling F#
    #Print blockchain info
    pass


def printMenu():
    print("1. Enter a new transaction.")
    print("2. Check current balance.")
    print("3. View unconfirmed transactions.")
    print("4. Print the last x number of confirmed transactions.")
    print("5. Print the blockchain.")
    print("End with any other input.")


def menuSelection():
    userSelection = input("Select an option:")
    if userSelection == '1':
        newTransaction()
        return 0
    elif userSelection == '2':
        currentBalance()
        return 0
    elif userSelection == '3':
        unconfirmedTX()
        return 0
    elif userSelection == '4':
        numOfTX = input("Enter number of confirmed transactions you wish to view:")
        confirmedTX(numOfTX)
        return 0
    elif userSelection == '5':
        printBlockchain()
        return 0
    else:
        return 1


def main():
    userQuit = 0
    while userQuit == 0:
        printMenu()
        userQuit = menuSelection()
    clientSocket.close()

if __name__== "__main__":
   main()


