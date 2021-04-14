from socket import socket 
from socket import AF_INET
from socket import SOCK_DGRAM
serverName = 'localhost'
serverPort = 10000
clientSocket = socket(AF_INET, SOCK_DGRAM)


def newTransaction():
    message = "Send TX to block."
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    returnMessage, serverAddress = clientSocket.recvfrom(2048)
    print("Message from Full Block: " + returnMessage.decode())


def currentBalance():
    pass


def unconfirmedTX():
    pass


def confirmedTX(numOfTX):
    pass


def printBlockchain():
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


