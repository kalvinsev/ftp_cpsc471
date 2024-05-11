from socket import *
import subprocess
import sys
import os

serverName = "127.0.0.1"
serverPort = int(sys.argv[1])

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
    files = subprocess.getstatusoutput('ls')[1].split('\n')
    if filename in files:
        with open(filename, 'rb') as file_obj:
            file_size = os.path.getsize(filename)
            # Send file size padded to 10 bytes
            connectionSocket.send(str(file_size).encode().ljust(10))  
            
            while True:
                # Read file in chunks of 64KB
                file_data = file_obj.read(65536)  
                if not file_data:
                    break
                # Send file data
                connectionSocket.sendall(file_data)  
            
            print("*SUCCESS* Client successfully downloaded files")
            success = f"*SUCCESS*\nSuccessfully downloaded '{filename}' as 'recv_from_server.txt'\nTotal bytes transferred: {file_size}"
            connectionSocket.send(success.encode())
            file_obj.close()
    else:
        print("*FAILURE*")
        response = f"'{filename}' not found in server. Use 'ls' to view the files present on the server."
        connectionSocket.send(response.encode())
    return

def put(filename):
    try: 
        
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
        fileSizeBuff = recvAll(connectionSocket, 10)
            
        # Get the file size
        fileSize = int(fileSizeBuff)
        
        print ("The file size is ", fileSize)
        
        # Get the file data
        fileData = recvAll(connectionSocket, fileSize)
        
        # print("The file data is: ")
        # print (fileData)

        with open("upload_from_client.txt", 'w') as file:
            file.write(fileData)
        file.close()
        print("*SUCCESS* File upload successful")
        success = f"*SUCCESS* File uploaded successfully as 'upload_from_client'\nTotal bytes transferred: {fileSize}"
        connectionSocket.send(success.encode())
    except Exception as e:
        print(f"{e} FAILURE")
    return

def ls():
    response = subprocess.getstatusoutput('ls')[1]
    # Send the response back to the client
    connectionSocket.send(response.encode())
    print("*SUCCESS* Client viewed files on server")
    return

# Port on which to listen to
serverPort = int(sys.argv[1])
# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# Bind the socket to the port 
serverSocket.bind(("", serverPort))
# Start listening for incoming connections
serverSocket.listen(1)

print("The server is ready to receive")

# The buffer to store the received data
data = ""

# Forever accept incoming connections
while True:
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(1024)
    arguments = data.decode().split() # ex: arguments = [get, file.txt] | [put, file.txt] | [ls]
    match arguments[0]:
        case "put":
            print("Requested 'put' command")
            put(arguments[1])
        case "get":
            print("Requested 'get' command")
            get(arguments[1])
        case "ls":
            print("Requested 'ls' command")
            ls()
        case _:
            continue
    connectionSocket.close()