from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 20000
clientSocket = socket(AF_INET, SOCK_DGRAM)


#   getClientAccountInfo()
#   reads account names from the balanceA.txt 
#   and returns them as an array
#
def getClientAccountInfo():
    #open balanceB.txt
    #extract user account from each line
    #store user accounts in an array
    #return array
    pass


#   sendClientAccountInfo
#   Function that retrives a client's accounts and sends them over the servers
#   to the other client, to be used in creating a new transaction
#   Sends an array of accounts to the other clients to be used as payees.
#
def sendClientAccountInfo():
    #call getClientAccountInfo
    #send array to F2 server
    pass


def newTransaction():
    message = "Send TX to block."
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    returnMessage, serverAddress = clientSocket.recvfrom(2048)
    print("Message from Full Block: " + returnMessage.decode())
        #=========================================
    #   To create a new Tx:
    #
    #   call getClientAccountInfo
    #   List to user and they select an account as payer
    #
    #   Send a server message to F2 to get clientA accounts through F2
    #   List retrieved account names to user to select as payee
    #
    #   User enters transaction amount
    #   Check if user entered amount + fee is more than payer account(unconfirmed balance)
    #   If true, break
    #   If not true, subtract amount + fee from unconfirmed balance
    #
    #   Store Tx information in variable as 12-byte hex
    #   Append tx to Unconfirmed_TxB.txt
    #   Send tx to F2 node


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


