import re
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


#   Test function to display server connection and communication
#
def clientTxCheckResponse(clientAddress):
    returnMessage = "TX Confirmed."
    serverSocket.sendto(returnMessage.encode(), clientAddress)
    print("Return Message Sent.")
    blockMessage = "TX Notification"
    F1Socket.sendto(blockMessage.encode(), (serverName, connectPortF1))
    print("Other Block Notified")


def mineBlock():
    # Hash header of last block and store in lastBlockHash
    # Create Merkle root from 4 Temp_B.txt tx
    # Use function in instructions to find nonce
    # Combine header and body and store as 116-byte Hex "newBlock"
    # return newBlock
    pass


def processTX():
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
    pass

def processBlock():
    # Apppend block to blockchain.txt
    # Remove Tx from Temp_B.txt
    # Check Tx and send confirmation to clientB
    # Exit
    pass


def main():
    while 1:
        print("F2 Working...")
        message, clientAddress = serverSocket.recvfrom(2048)
        incomingMessage = message.decode()

        #
        # Check if the message is a transaction or a block (format)
        # 
        # If transaction, call processTX()
        # If else is block, call processBlock()
        # If else clientPayeeRequest, send message to F2 for client list
        # If else serverPayeeRequest, send message to clientA to request clientA accounts
        # If else f2ListToClient, pass F2 client list to clientA
        # If else clientListToF2, pass clientA list to F2

        clientTxCheck = re.search("Send TX to block.", incomingMessage)
        serverNotifCheck = re.search("TX Notification", incomingMessage)
        if clientTxCheck != None:
            clientTxCheckResponse(clientAddress)
        elif serverNotifCheck != None:
            print("TX Notification Recieved from Block 1")
        else:
            pass

if __name__== "__main__":
   main()