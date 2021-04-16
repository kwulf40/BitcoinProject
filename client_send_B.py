import pathlib
import fileinput
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


def verifyBalance(payer, txAmount):
    totalAmount = txAmount + 2

    clientBFile = pathlib.Path("balanceB.txt")
    if clientBFile.exists():
        activeBalanceB = open(clientBFile, "r")
    if activeBalanceB.mode == 'r':
        for account in activeBalanceB:
            acctVar = account.split(":")
            if acctVar[0] == payer:
                unconfirmedBal = int(acctVar[1], 16)
                checkBalance = unconfirmedBal - totalAmount
                if checkBalance < 0:
                    print("Not enough funds in Account: " + payer)
                    return 0
                else:
                    return 1
            else:
                pass
        return 0
    else:
        print("Error with file")

def reduceUnconfirmedBal(payer, txAmount):
    totalTxAmount = txAmount + 2
    modifiedFlag = 0
    modifiedBalance = "balanceB.txt"
    with fileinput.FileInput(modifiedBalance, inplace=True, backup='.bak') as file:
        for line in file:
            tempAcctInfo = str(line)
            acctVar = line.split(":")
            if acctVar[0] == payer:
                newAcctVar = []
                unconfirmedBal = int(acctVar[1], 16)
                newBal = unconfirmedBal - totalTxAmount
                newAcctVar.append(payer)
                newAcctVar.append(str('%08X' % newBal))
                newAcctVar.append(acctVar[2])
                newAcctInfo = (newAcctVar[0] + ":" + newAcctVar[1] + ":" + newAcctVar[2])
                print(line.replace(tempAcctInfo, newAcctInfo), end='')
                modifiedFlag = 1
            else:
                print(line, end='')
    file.close()
    if modifiedFlag:
        return 1
    else:
        return 0


def newTransaction():
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

    print("Getting Account Numbers\n")
    accounts = getClientAccountInfo()

    x = 1
    for ID in accounts:
        print("Account Number: " + ID)
        x += 1

    payerAcct = input("Select a Payer Account:")
    payerAcct = int(payerAcct)
    payer = accounts[payerAcct - 1]

    print("Requesting Payee Accounts\n")
    message = "Request F1 Accounts"
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    returnedAccounts, serverAddress = clientSocket.recvfrom(2048)
    returnedAccounts = returnedAccounts.decode()
    payeeAccounts = returnedAccounts.split(":")

    y = 1
    for ID in payeeAccounts:
        print("Account Number: " + ID)
        y += 1

    payeeAcct = input("Select a Payee Account:")
    payeeAcct = int(payeeAcct)
    payee = payeeAccounts[payeeAcct - 1]

    txAmount = input("Input Transaction Amount: ")
    txAmount = int(txAmount)
    
    txHex = str(payer) + str(payee) + str('%08X' % txAmount)
    verify = verifyBalance(payer, txAmount)
    if verify:
        complete = reduceUnconfirmedBal(payer, txAmount)
        if complete:
            unconfirmedTxBFile = pathlib.Path("Unconfirmed_TxB.txt")
            newUnconfirmed = open(unconfirmedTxBFile, "w+")
            newUnconfirmed.write(txHex + "\n")
            newUnconfirmed.close()
            clientSocket.sendto(txHex.encode(), (serverName, serverPort))
            print("Tx Complete")
        else:
            print("Tx Failed")
    else:
        print("Verify Failed")


# Prints the account name, unconfirmed balance, and confirmed balance
# for each account in balanceB.txt
def currentBalance():
    #Get account info from balanceA.txt
    clientBFile = pathlib.Path("balanceB.txt")
    if clientBFile.exists():
        activeBalanceB = open(clientBFile, "r")
    else: 
        print("Error finding balance file")
        return 0
    

    #loop for each account
    if activeBalanceB.mode == 'r':
        for account in activeBalanceB:
            acctVar = account.split(":")
            unconfirmedBal = int(acctVar[1], 16)
            confirmedBal = int(acctVar[2], 16)
            #Print account name
            #print unconfirmed balance
            #print confirmed balance
            print("Account Number: " + acctVar[0])
            print("Uncomfirmed Balance: " + str(unconfirmedBal))
            print("Comfirmed Balance: " + str(confirmedBal) + "\n")
        return 1
    else:
        print("File Read Error")
        return 0


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
    getClientAccountInfo()
    userQuit = 0
    while userQuit == 0:
        printMenu()
        userQuit = menuSelection()
    clientSocket.close()

if __name__== "__main__":
   main()


