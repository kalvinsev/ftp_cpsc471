from socket import *
import sys
import os
import time
# Name and port number of the server to which you want to connect
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

def recvAll(sock, numBytes):
    
    # The buffer
    recvBuff = ""
	
	# The temporary buffer
    tmpBuff = ""
	
	# Keep receiving till all is received
    while len(recvBuff) < numBytes:	
		# Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)
		
		# The other side has closed the socket
        if not tmpBuff:
            break
		# Add the received bytes to the buffer
        recvBuff += tmpBuff.decode()
    return recvBuff

def get(filename): 
    # Create a socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # # Connect to server
    clientSocket.connect((serverName, serverPort))
    # String we want to send to the server
    data = "get " + filename
    bytesSent = 0
    # Send message
    clientSocket.send(data.encode())
    # The buffer to all data received from the
    # the client.
    fileData = ""
    # The temporary buffer to store the received
    # data.
    recvBuff = ""
    # The size of the incoming file
    fileSize = 0	
    # The buffer containing the file size
    fileSizeBuff = ""
    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(clientSocket, 10)
        
    # Get the file size
    fileSize = int(fileSizeBuff)
    
    # print (f"*SUCCESS*\nSuccessfully downloaded '{filename}' as recv_from_server.txt\nTotal bytes transferred {fileSize}")
    # Get the file data
    fileData = recvAll(clientSocket, fileSize)
    
    # print("The file data is: ")
    # print (fileData)
    
    with open("recv_from_server.txt", 'w') as file:
        file.write(fileData)
    # Capture server response
    response = clientSocket.recv(1024).decode()
    print(response)
    clientSocket.close()

    return

def put(filename):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect to server
    clientSocket.connect((serverName, serverPort))
    data = "put " + filename
    bytesSent = 0
    # Send message
    clientSocket.send(data.encode())

    if os.path.exists(filename):
        with open(filename, 'rb') as file_obj:
            file_size = os.path.getsize(filename)
            # Send file size padded to 10 bytes
            clientSocket.send(str(file_size).encode().ljust(10))  
            
            while True:
                # Read file in chunks of 64KB
                file_data = file_obj.read(65536)  
                if not file_data:
                    break
                # Send file data
                clientSocket.sendall(file_data)  
            
            file_obj.close()
        response = clientSocket.recv(1024).decode()
        print(response)
        clientSocket.close()
    else:
        print("You must ensure the file is present in the same directory where this program lives")

    return

def ls():
    try: 
        # Create a socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # # Connect to server
        clientSocket.connect((serverName, serverPort))
        # String we want to send to the server
        data = "ls"
        bytesSent = 0
        # Send message
        while bytesSent != len(data):
            bytesSent += clientSocket.send(data[bytesSent:].encode())
        response = clientSocket.recv(1024).decode()
        print("List of files on the server: ")
        for file in response.split('\n'):
            print(f"- {file}")
        # Terminate connection
        clientSocket.close()
    except Exception as e:
        print(f"{e} FAILURE")

    return

def main():
    print("*Welcome to File Transer Protocol*")
    print("Use 'get <FILENAME>', 'put <FILENAME>', or 'ls' without quotes to upload, download, or view files to/from the sberver.\nEnter 'quit' to terminate the session.")
    arguments = [""]
    while arguments[0] != "quit":
        cmd = input("ftp> ")
        arguments = cmd.split()
        # Valid argument check
        if len(arguments) < 2 and (arguments[0] == "get" or arguments[0] == "put"): 
            print("USAGE python " + sys.argv[0] + "<FILE NAME>")
            continue

        match arguments[0]:
            case "put":
                put(arguments[1])
            case "get":
                get(arguments[1])
            case "ls":
                ls()
            case "quit":
                print("Exiting ...")
                break
            case _:
                print("Please enter a valid argument.")
                
    return 0

if __name__ == "__main__":
    main()