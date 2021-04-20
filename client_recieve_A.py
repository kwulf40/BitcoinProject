import re
import pathlib
import fileinput
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


def verifyTx(transaction):
    # If payer:
    # Verify Tx with corresponding TX in Unconfirmed_TxA.txt
    # Reduce Tx amount + Tx fee from account's confirmed balance
    # Removes Tx from Unconfirmed_TxA.txt
    # Appends Tx to Confirmed_TxA.txt
    #
    # If payee:
    # Adds Tx amount to account's confirmed and unconfirmed balance.
    # Appends Tx to Confirmed_TxA.txt


    verify = 0
    if str(transaction)[0] == 'A':
        #Is payer
        #open Unconfirmed_TxA.txt
        unconfirmedTxAFile = pathlib.Path("Unconfirmed_TxA.txt")
        if unconfirmedTxAFile.exists():
            activeUnconfirmedA = open(unconfirmedTxAFile, "r")
            #verify tx 
            for line in activeUnconfirmedA:
                if str(line).strip("\n") == str(transaction):
                    verify = 1
                else:
                    pass
            activeUnconfirmedA.close()
        else:
            print("Error, no Unconfirmed_TxA to read")
        if verify == 1:
            #if verified, reduce confirmed balance by tx amount
            txAmount = int(str(transaction)[16:], 16) + 2
            payer = str(transaction[0:8])
            modifiedBalance = "balanceA.txt"
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
            unconfirmedTxAFile = pathlib.Path("Unconfirmed_TxA.txt")
            activeUnconfirmedA = open(unconfirmedTxAFile, "r")
            unconfirmedTx = activeUnconfirmedA.readlines()
            activeUnconfirmedA.close()

            newUnconfirmed = open(unconfirmedTxAFile, "w")
            lineCheck = 0
            for tx in unconfirmedTx:
                if tx.strip("\n") != str(transaction):
                    newUnconfirmed.write(tx)
                elif tx.strip("\n") == str(transaction) and lineCheck < 1:
                    lineCheck += 1
                else:
                    newUnconfirmed.write(tx)
            newUnconfirmed.close()

            # Appends Tx to Confirmed_TxA.txt
            confirmedFile = pathlib.Path("Confirmed_TxA.txt")
            openConfA = open(confirmedFile, "a+")
            openConfA.write(str(transaction) + "\n")
            openConfA.close()
        else:
            print("Verification failed")
    else:
        #Is payee
        txAmount = int(str(transaction)[16:], 16)
        payee = str(transaction[8:16])
        modifiedBalance = "balanceA.txt"
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
        # Appends Tx to Confirmed_TxA.txt
        confirmedFile = pathlib.Path("Confirmed_TxA.txt")
        openConfA = open(confirmedFile, "a+")
        openConfA.write(str(transaction) + "\n")
        openConfA.close()


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
        # accountInfoRequest will be true if the incoming message is a request for the Client A accounts from F1
        #
        accountInfoRequest = re.search("Request Client A Accounts", incomingMessage)
        transactionCheck = re.match(r'(^([A-B])([0]{6})([1-2]))', incomingMessage)
        #if-elif to check the true-false value of each message checks
        #if accountInfoRequest is true, sends client A account info to F1
        if accountInfoRequest:
            accountString = sendClientAccountInfo()
            serverSocket.sendto(accountString.encode(), clientAddress)
            print("Client A Info Sent")
        # on received tx to confirm from block chain,
        # call verifyTx()
        elif transactionCheck:
            print("Confirmed Tx recieved from server: " + str(incomingMessage))
            verifyTx(incomingMessage)
        else:
            pass


if __name__== "__main__":
   main()