from socket import *
import subprocess
import sys

def get(filename):
    files = subprocess.getstatusoutput('ls')[1].split('\n')

    if filename in files:
        # print('filename in files')
        connectionSocket.send("filename in files".encode())
        """TODO:"""
    else:
        print("*FAILURE*")
        response = f"'{filename}' not found in server. Use 'ls' to view the files present on the server."
        connectionSocket.send(response.encode())


    

def ls():
    response = subprocess.getstatusoutput('ls')[1]
    # Send the response back to the client
    connectionSocket.send(response.encode())
    print("*SUCCESS*")

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
    data = connectionSocket.recv(40)
    arguments = data.decode().split()
    match arguments[0]:
        case "get":
            print("Requested 'get' command")
            get(arguments[1])
        case "put":
            print("Requested 'put' command", end=" ")
        case "ls":
            print("Requested 'ls' command", end=" ")
            ls()
        case _:
            continue
    connectionSocket.close()

    
