'''
CLASS DESCRIPTION:
The server can accept 1 client connection and send/receive
simple string messages using TCP/IP. The client can choose to
disconnect at any time.

MESSAGES SENT:

(field)   (bytes num)    (desc)
header     4              Number of data bytes following the header
data       1 - int max    Protocol has not been determined yet

TODO:
~ Test if there can be multiple clients communicating to this
    server, or if there is a max of 2 participants.
'''

import sys
import os
import struct
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

bytepack = struct.pack('>I', 12345)
message = struct.unpack('>I', bytepack)
print(str(message))

'''
SUMMARY
Parse through the data received from the socket
and return the variable amount of data.

OUTPUTS
(byte string) Data received from the socket.
'''
def read_msg(sock):

    # Try to pull a byte from the socket
    # and return status = false if no connection.
    rawMsgLen = recv_all(sock, 4)
    if not rawMsgLen:
        return None

    # if unparsed data was pulled from the socket,
    # read the number of bytes that the header
    # says there was in big-endian network order.
    msgLen = struct.unpack('>I', rawMsgLen)[0]
    
    return recv_all(sock, msgLen) 

'''
SUMMARY
Receive a variable number of bytes from the
socket as a byte string.

OUTPUTS
data - (byte string) Data received from the socket.
'''
def recv_all(sock, num_bytes):
    
    # Receive variable number of TCP packets from the
    # socket and store into the byte string "data"
    data = b''
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))

        # if no data was received from the socket
        # return an empty packet
        if not packet:
            return None

        # otherwise, add to the byte string
        data += packet

    # Once all the data  has been received,
    # exit the loop and return the data.
    return data

'''
SUMMARY
Write a variable number of bytes to the socket.

INPUTS
msg - (byte) data to send out to the socket.
'''
def write_msg(sock, msg):

    # package the message with a header indicating
    # that the length of the message (up to 4 bytes)
    # ordered in big-endian network byte order (>).
    # Then, send the data to the socket.
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                    IPC SERVER CLASS
# ==                                                          ==
# ==============================================================
# ==============================================================

'''
SUMMARY:
This class is used as a common resource between multiple python
instances. Data can be both sent and received.
'''
class IPCServer:

    def __init__(self, port):

        # initialize instance parameters
        self.authkey = os.urandom(20)
        self.listener = None
        self.conn = None
        self.connectionStatus = False

        # call setup methods
        self.listener, self.conn = self.__SetupConnection(port)

    def __exit__(self):

        # close down the communication port if exiting scope
        self.Close()

    '''
    SUMMARY
    Initialize a socket with an IPv4 address on the passed
    port.

    INPUTS
    port - (int) Port that the socket will be opened at on the
    listener AND speaker sides.

    OUTPUTS
    conn - socket for receiving data
    '''
    def __SetupConnection(self, port):

        # Create a connection socket to communicate through
        address = ('localhost', port)
        listener = Listener(address)
        conn = listener.accept()

        self.TermPrint("Connection successful")
        
        # return the connection socket
        return listener, conn

    def Write(self, msg):
        write_msg(self.conn, msg)

    def Read(self):
        return read_msg(self.conn)

    '''
    SUMMARY
    Close down the connection socket if one is open. Always close
    down the listener socket.
    '''
    def Close(self):
        self.listener.close()
        self.TermPrint("Listener socket closed.")
        
        self.conn.close()
        self.TermPrint("Connection socket closed.")

    def TermPrint(self, message):
        print("*** IPC SERVER *** : " + message)

# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                    IPC CLIENT CLASS
# ==                                                          ==
# ==============================================================
# ==============================================================
'''
SUMMARY:
This class is used as a common resource between multiple python
instances. Data can be both sent and received.
'''
class IPCClient:

    def __init__(self, port):

        # initialize instance parameters
        self.conn = None
        self.connectionStatus = False

        # call setup methods
        self.conn = self.__SetupConnection(port)

    def __exit__(self):

        # close down the communication port if exiting scope
        self.Close()

    '''
    FUNCTION
    __SetupConnection
    
    SUMMARY
    Initialize a socket with an IPv4 address on the passed
    port.

    INPUTS
    port - (int) Port that the socket will be opened at on the
    listener AND speaker sides.

    OUTPUTS
    conn - socket for receiving data
    '''
    def __SetupConnection(self, port):

        # Create a connection socket to communicate through
        address = ('localhost', port)
        conn = Client(address)
        
        self.TermPrint("Connection successful")
        
        # return the connection socket
        return conn

    def Write(self, msg):
        write_msg(self.conn, msg)

    def Read(self):
        return read_msg(self.conn)

    '''
    FUNCTION
    Close
    
    SUMMARY
    Close down the connection socket if one is open. Always close
    down the listener socket.
    '''
    def Close(self):
        self.conn.close()
        self.TermPrint("Connection socket closed.")

    def TermPrint(self, message):
        print("*** IPC CLIENT *** : " + message)
