from socket import *
import sys

# Name and port number of the server to which you want to connect
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

def connect():
    return

def get(filename):
    """
    'get' command
    TODO:
        retreive file
        1) first make a request to server and check if the file exits (server side)
            if the file does not exist:
                    send a message to client indicating file DNE
            else prepare this function to retreive file
        2) prepare server side to send file
    """
    try: 
        # Create a socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # # Connect to server
        clientSocket.connect((serverName, serverPort))
        # String we want to send to the server
        data = "get " + filename
        bytesSent = 0
        # Send message
        while bytesSent != len(data):
            bytesSent += clientSocket.send(data[bytesSent:].encode())
        response = clientSocket.recv(1024).decode()
        print(response)
        # for file in response.split('\n'):
        #     print(f"\t{file}")
        # Terminate connection
        clientSocket.close()
    except Exception as e:
        print(f"{e} FAILURE")

    return

def put():
    """
    'put' command
    TODO:
        upload file
        1) first connect to server
        2) prepare connection file file transfer
        3) handle server file on serverside
        
    """
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
    print("Use 'get <FILENAME>', 'put <FILENAME>', or 'ls' without quotes to upload, download, or view files to/from the server.\nEnter 'quit' to terminate the session.")
    arguments = [""]
    while arguments[0] != "quit":
        cmd = input("ftp> ")
        arguments = cmd.split()
        # Valid argument check
        if len(arguments) < 2 and arguments[0] == "get" or arguments[0] == "put": 
            print("USAGE python " + sys.argv[0] + "<FILE NAME>")
            continue

        match arguments[0]:
            case "put":
                print("You would like to upload a file!")
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