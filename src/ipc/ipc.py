'''
CLASS DESCRIPTION:
The server can accept 1 client connection and send/receive
simple string messages using TCP/IP. The client can choose to
disconnect at any time.

TODO:
~ Test if there can be multiple clients communicating to this
    server, or if there is a max of 2 participants.
'''

import sys
import os

import struct
import socket

from multiprocessing.connection import Listener
from multiprocessing.connection import Client
    
# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                        SOCKET METHOD
# ==                                                          ==
# ==============================================================
# ==============================================================
'''
SUMMARY
Receive data from the socket. This function allows
the user to control how much data is requested from
the socket.
'''
def read_msg_sock(sock):

    # Read message length and unpack it into an integer
    raw_msglen = recvall_sock(sock, 4)
    if not raw_msglen:
        return None

    msglen = struct.unpack('>I', raw_msglen)[0]

    # Read the message data
    return recvall_sock(sock, msglen)

def recvall_sock(sock, n):

    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:

        packet = sock.recv(n - len(data))

        if not packet:
            return None

        data += packet
    return data

'''
SUMMARY
Write a user-defined number of bytes to the socket.

INPUTS
msg - (byte) data to send out to the socket.
'''
def write_msg_sock(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

class SocketServer:
    
    def __init__(self, port):

        # initialize instance parameters
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

        # Create a socket to listen for connections
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('', port))
        listener.listen(1)

        # Connection socket for communication
        conn, conn_addr = listener.accept()
        self.TermPrint("Connection with " + sock_addr)
        
        # return the connection socket
        return listener, conn

    def Write(self, msg):
        write_msg_sock(self.conn, msg)

    def Read(self):
        return read_msg_sock(self.conn)

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

class SocketClient:
    def __init__(self, ipv4_addr, port):

        # initialize instance parameters
        self.conn = None
        self.connectionStatus = False

        # call setup methods
        self.conn = self.__SetupConnection(ipv4_addr, port)

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
    def __SetupConnection(self, ipv4_addr, port):

        # Create a connection socket to communicate through
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('255.255.255.255', port))
        self.TermPrint("Connection successful")
        
        # return the connection socket
        return conn

    def Write(self, msg):
        write_msg_sock(self.conn, msg)

    def Read(self):
        return read_msg_sock(self.conn)

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

# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                    MULTITHREAD METHOD
# ==                                                          ==
# ==============================================================
# ==============================================================

# +----------+----------+----------+----------+----------+
# |                    GENERIC FUNCTIONS                 |
# +----------+----------+----------+----------+----------+
'''
SUMMARY
Receive data from the socket.

UPDATES:
~ Find a way to control the amount of data we receive
    so we can develop a more controlled protocol for
    parsing through the data. In the future, the following
    message protocol may be more practical...

    (field)   (bytes num)    (desc)
    header     4              Number of data bytes following the header
    data       1 - int max    Protocol has not been determined yet

OUTPUTS
(byte string) Data received from the socket.
'''
def read_msg(sock):

    # Try to read data from the socket and
    # return None if there is no data.
    rx = sock.recv()
    if not rx:
        return None
    
    return rx

'''
SUMMARY
Write a variable number of bytes to the socket.

INPUTS
msg - (byte) data to send out to the socket.
'''
def write_msg(sock, msg):
    sock.send(msg)

# +----------+----------+----------+----------+----------+
# |                    IPC SERVER CLASS                  |
# +----------+----------+----------+----------+----------+
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

# +----------+----------+----------+----------+----------+
# |                    IPC CLIENT CLASS                  |
# +----------+----------+----------+----------+----------+
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

# +----------+----------+----------+----------+----------+
# |                         MAIN                         |
# +----------+----------+----------+----------+----------+
if __name__ == '__main__': main()
