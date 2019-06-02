'''
CLASS DESCRIPTION:
The server can accept 1 client connection and send/receive
simple string messages using TCP/IP. The client can choose to
disconnect at any time.

TODO:
~ self.connectionStatus needs to update to be True if __SetupConnection
    was successful
'''

import sys
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

# ==============================================================
# ==============================================================
# ==                                                          ==
# ==                IPC MULTITHREADING METHOD           
# ==                                                          ==
# ==============================================================
# ==============================================================

class IPCListener:

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
        listener = Listener(address, authkey=b'password')
        conn = listener.accept()

        self.TermPrint("Connection successful")
        
        # return the connection socket
        return listener, conn

    '''
    FUNCTION
    Read
    
    SUMMARY
    Read the next available value in the socket.
    Currently no way of controlling how many bytes are received.

    INPUTS
    None

    OUTPUTS
    status - (bool) if True, connection is still valid.
    rx - (??) Data received from the socket.
    '''
    def ReadByte(self):
        status = True

        # Try to pull a byte from the socket
        # and return status = false if no connection.
        rx = self.conn.recv(8)
        if not rx:
            rx = 0
            status = False
        
        return status, rx

    '''
    FUNCTION
    Close
    
    SUMMARY
    Close down the connection socket if one is open. Always close
    down the listener socket.

    INPUTS
    None

    OUTPUTS
    None
    '''
    def Close(self):
        self.listener.close()
        self.TermPrint("Listener socket closed.")
        
        self.conn.close()
        self.TermPrint("Connection socket closed.")

    def TermPrint(self, message):
        print("*** IPCLISTENER *** : " + message)

class IPCSpeaker:

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
        conn = Client(address, authkey=b'secret password')
        
        self.TermPrint("Connection successful")
        
        # return the connection socket
        return conn

    '''
    FUNCTION
    Read
    
    SUMMARY
    Read the next available value in the socket.
    Currently no way of controlling how many bytes are received.

    INPUTS
    tx - (byte) data to send out to the socket.

    OUTPUTS
    None
    '''
    def WriteByte(self, tx):
        self.conn.send(tx)

    '''
    FUNCTION
    Close
    
    SUMMARY
    Close down the connection socket if one is open. Always close
    down the listener socket.

    INPUTS
    None

    OUTPUTS
    None
    '''
    def Close(self):
        self.conn.close()
        self.TermPrint("Connection socket closed.")

    def TermPrint(self, message):
        print("*** IPCSPEAKER *** : " + message)
