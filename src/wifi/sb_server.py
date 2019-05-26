# FILE DESCRIPTION:
# The server can accept 1 client connection and send/receive
# simple string messages using TCP/IP. The client can choose to
# disconnect at any time.

# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                    IMPORT DEPENDENCIES             
# ==                                                          ==
# ==============================================================
# ==============================================================
import socket
import sys
from timeit import default_timer as timer

# ====================== CACHED DATA ======================
storedValue = "SERVER: Test String"
host = ''
port = 5560

# ======================== FUNCTIONS ======================
# DESC: This function sets up the socket for server-side
#       communication.
# RETURNS: socket.socket
def SetupServer():
    # AF_INET = address family, APv4 requires (host, port) tuple
    # SOCK_STREAM = socket expects TCP packets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")

    # Bind the socket to an address so the server
    # can accept client connections.
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete")

    return s


# DESC: This function allows 1 client to connect at a time.
# RETURNS: connection = new socket for send/receive communication
def SetupConnection(s):
    # Allows 1 connection.
    s.listen(1)

    # Create a new socket "connection" that allows send/receive
    # from the address tied to the other side of the socket.
    connection, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return connection


# Get the cached value to be sent.
def GET():
    reply = storedValue
    return reply


# Send back the remaining portion of data
# from the command/data combo.
def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply


# DESC: This function sends/receives data until told not to.
def DataTransfer(connection, sock):
    while True:

        # RECEIVE THE DATA ---------------------------------
        #start = timer()
        data = connection.recv(1024)
        data = data.decode('utf-8')
        #end = timer()
        #print("Data Receive/Decode time(s): " + (end - start))

        # Split the data to separate the command from the
        # rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]

        # Decode the command received by the server from the client
        # Send the currently cached string.
        if command == 'GET':
            reply = GET()

        # Repeat the previous data message.
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)

        # Go back to the beginning of the loop
        # and listen for another client connection.
        elif command == 'EXIT':
            print("Client has exited..")
            break

        # Shut down the server by closing the ORIGINAL socket.
        # End of the program.
        elif command == 'KILL':
            print("Server shutting down..")
            sock.close()
            break

        # Handle unknown commands.
        else:
            reply = 'Unknown command..'

        # SEND DATA TO CLIENT --------------------------------
        #start = timer()
        connection.sendall(str.encode(reply))
        #end = timer()
        print("Data has been send..")
        #print("Data Encode/Transfer time(s): " + (end - start))

    # If the while loop is exited by the KILL/EXIT commands,
    # close the second communication socket.
    connection.close()


# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                    STAND ALONE             
# ==                                                          ==
# ==============================================================
# ==============================================================
if __name__ == "__main__":

    print(sys.version)
    s = SetupServer()

    while True:
        try:
            conn = SetupConnection(s)
            DataTransfer(conn, s)
        except:
            break
