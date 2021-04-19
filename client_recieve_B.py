import re
import pathlib
import fileinput
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


def verifyTx(transaction):
    # If payer:
    # Verify Tx with corresponding TX in Unconfirmed_TxB.txt
    # Reduce Tx amount + Tx fee from account's confirmed balance
    # Removes Tx from Unconfirmed_TxB.txt
    # Appends Tx to Confirmed_TxB.txt
    #
    # If payee:
    # Adds Tx amount to account's confirmed and unconfirmed balance.
    # Appends Tx to Confirmed_TxB.txt


    verify = 0
    if str(transaction)[0] == 'B':
        #Is payer
        #open Unconfirmed_TxB.txt
        unconfirmedTxBFile = pathlib.Path("Unconfirmed_TxB.txt")
        if unconfirmedTxBFile.exists():
            activeUnconfirmedB = open(unconfirmedTxBFile, "r")
            #verify tx 
            for line in activeUnconfirmedB:
                if str(line).strip("\n") == str(transaction):
                    verify = 1
                else:
                    pass
            activeUnconfirmedB.close()
        else:
            print("Error, no Unconfirmed_TxA to read")
        if verify == 1:
            #if verified, reduce confirmed balance by tx amount
            txAmount = int(str(transaction)[16:], 16) + 2
            payer = str(transaction[0:8])
            modifiedBalance = "balanceB.txt"
            with fileinput.FileInput(modifiedBalance, inplace=True) as file:
                for line in file:
                    tempAcctInfo = str(line)
                    acctVar = line.split(":")
                    if acctVar[0] == payer:
                        newAcctVar = []
                        confirmedBal = int(acctVar[2], 16)
                        newBal = confirmedBal - txAmount
                        newAcctVar.append(payer)
                        newAcctVar.append(acctVar[1])
                        newAcctVar.append(str('%08X' % newBal))
                        newAcctInfo = (newAcctVar[0] + ":" + newAcctVar[1] + ":" + newAcctVar[2]  + "\n")
                        print(line.replace(tempAcctInfo, newAcctInfo), end='')
                    else:
                        print(line, end='')
            file.close()

            # Removes Tx from Unconfirmed_TxA.txt
            unconfirmedTxBFile = pathlib.Path("Unconfirmed_TxB.txt")
            activeUnconfirmedB = open(unconfirmedTxBFile, "r")
            unconfirmedTx = activeUnconfirmedB.readlines()
            activeUnconfirmedB.close()

            newUnconfirmed = open(unconfirmedTxBFile, "w")
            for tx in unconfirmedTx:
                if tx.strip("\n") != str(transaction):
                    newUnconfirmed.write(tx)
            newUnconfirmed.close()

            # Appends Tx to Confirmed_TxA.txt
            confirmedFile = pathlib.Path("Confirmed_TxB.txt")
            openConfB = open(confirmedFile, "a+")
            openConfB.write(str(transaction) + "\n")
            openConfB.close()
        else:
            print("Verification failed")
    else:
        #Is payee
        txAmount = int(str(transaction)[16:], 16)
        payee = str(transaction[8:16])
        modifiedBalance = "balanceB.txt"
        with fileinput.FileInput(modifiedBalance, inplace=True) as file:
            for line in file:
                tempAcctInfo = str(line)
                acctVar = line.split(":")
                if acctVar[0] == payee:
                    newAcctVar = []
                    unconfirmedBal = int(acctVar[1], 16)
                    confirmedBal = int(acctVar[2], 16)
                    newUnconfBal = unconfirmedBal + txAmount
                    newConfBal = confirmedBal + txAmount
                    newAcctVar.append(payee)
                    newAcctVar.append(str('%08X' % newUnconfBal))
                    newAcctVar.append(str('%08X' % newConfBal))
                    newAcctInfo = (newAcctVar[0] + ":" + newAcctVar[1] + ":" + newAcctVar[2] + "\n")
                    print(line.replace(tempAcctInfo, newAcctInfo), end='')
                else:
                    print(line, end='')
            file.close()
        # Appends Tx to Confirmed_TxB.txt
        confirmedFile = pathlib.Path("Confirmed_TxB.txt")
        openConfB = open(confirmedFile, "a+")
        openConfB.write(str(transaction) + "\n")
        openConfB.close()


def main():
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()
        
        #
        # regex function calls to identify incoming message
        #
        # transationCheck will be true if the first 8 digits of the incoming message are 
        # in the format of a client account, signaling an incoming transactions
        #
        # accountInfoRequest will be true if the incoming message is a request for the Client B accounts from F2
        #
        accountInfoRequest = re.search("Request Client B Accounts", incomingMessage)
        transactionCheck = re.match(r'(^([A-B])([0]{6})([1-2]))', incomingMessage)
        #if-elif to check the true-false value of each message checks
        #if accountInfoRequest is true, sends client B account info to F2
        if accountInfoRequest:
            accountString = sendClientAccountInfo()
            serverSocket.sendto(accountString.encode(), clientAddress)
            print("Client B Info Sent")
        # on received tx to confirm from block chain,
        # call verifyTx()
        elif transactionCheck:
            verifyTx(incomingMessage)
        else:
            pass


if __name__== "__main__":
   main()