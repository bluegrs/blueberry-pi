'''
CLASS DESCRIPTION:
The client searches for a host to send data to the server.
It can also receive responses from the host for updating status.
Currently, these are the client's possible commands..

READ			=> Read the data stored in the server's self.stored
WRITE			=> Write a new string to the server's self.stored
REPEAT XXXXXX 	=> Tells the server to repeat the 'XXXXXX' message back to the client
EXIT			=> Client is disconnecting from the server
KILL			=> Client is telling the server to shut down

NOTES:
As shown in the MAIN() example located at the bottom of the file, 
the only functions required to run the client after instantiating
the object is DataTxToHost.
'''

import socket
import sys
import json
import subprocess 

class client: # ||| Protocol Communication Class |||
        
    def __init__(self, port, timeout):
        self.conn = self.__setup_connection(port, timeout)
        
    def __exit__(self):
        self.close()

    # +----------+----------+----------+----------+----------+
	# |                    PRIVATE METHODS                   |
	# +----------+----------+----------+----------+----------+
    
    ''' 
    SUMMARY: 
    Search all LAN IPs for a valid connection on the user defined
    port. Using IPv4 address family and TCP/IP.
    
    RETURN:
    conn - (socket.socket) connection socket to host.
    '''
    def __setup_connection(self, port, timeout):
    
        sock = None
        lan = "192.168.1."
  
        # Test all 256 LAN IPs and return the socket if
        # a valid connection is made.
        for ping in range(0,255): 
            address = lan + str(ping) 
            
            # Set up socket for communicating to server with IPv4, TCP/IP
            socketInfo = (address, port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # Try to connect to the port at this address. If a timeout
            # occurs, this was not the server's IP.
            try:
                sock.connect((address, port)) # Timeout reset
                sock.settimeout(None)
                break
                
            except:
                # Only update the user occasionally
                if ping % 100 == 0:
                    print("Searching for connection..")
                
        return sock

	# +----------+----------+----------+----------+----------+
	# |                     PUBLIC METHODS                   |
	# +----------+----------+----------+----------+----------+

    '''
    SUMMARY:
    User can request accel, gyro, and mag data using the cfg.ACCEL,
    cfg.GYRO, and cfg.MAG values. The data is returned as a floating
    point value.

    RETURN:
    x, y, z tuple containing floating point values from the sensor.
    '''
    def request(self, req):

        # send the request to the server as a single byte
        self.conn.send(req.encode('utf-8'))

        # receive the data from the server
        msgLength = self.conn.recv(4)
        data = self.conn.recv(int(msgLength))

        # decode the json.dump
        decoded = json.loads(data.decode('utf-8'))
        x = decoded.get("x")
        y = decoded.get("y")
        z = decoded.get("z")

        return x,y,z
        
    ''' SUMMARY: Close the connection socket made. '''
    def close(self):
        try:
            self.sock_conn.close()
            print("Connection closed.") 
        except:
            print("No connection to close.")

class wifi_client: # ||| Basic Communication Class |||
	
    def __init__(self, port):

        self.host = '192.168.1.26'
        self.port = port
        self.sock_conn = None

        # Setup the socket from the port number provided
        self.__SetupClient()

    # +----------+----------+----------+----------+----------+
    # |                    PRIVATE METHODS                   |
    # +----------+----------+----------+----------+----------+
	
    # NOTE: Check IP address when switching over to Wi-Fi.
    # NOTE: Test if this has to be the same port as the one
    # 		on the server side.
    def __GetClientSocketInfo(self):
        return self.host, self.port

    # DESC: Set up the client-side socket for TCP packets
    # RETURNS: socket.socket
    def __SetupClient(self):
    	socket_data_tuple = self.__GetClientSocketInfo()

    	# Set up a socket for communicating to the server
    	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.connect(socket_data_tuple)
    	print("Connection to server was successful")

    	self.sock_conn = sock
		
	# +----------+----------+----------+----------+----------+
	# |                     PUBLIC METHODS                   |
	# +----------+----------+----------+----------+----------+

	# DESC: Decodes the command to be sent to the server
	#		and returns the response.
	# RETURNS: boolean to break or not
    def DataTxToHost(self, message):

    	# Determine if the data transfer should continue or
    	# if the socket should close down
    	closeConnection = False
    	command = message.split(' ', 1)[0]

    	# Decode the command ------------------
    	# Send the EXIT request to other end
    	# and exit the connection.
    	# Send KILL command to shut down the server.
    	# Same behavior on client side.
    	if command == 'EXIT' or command == 'KILL':
    		closeConnection = True

    	# If other command, just send the command
    	# and wait for the response.
    	self.sock_conn.send(str.encode(message))
    	if not closeConnection:
    		reply = self.sock_conn.recv(1024)
    		print(reply.decode('utf-8'))

    	# If the client requests to disconnect using the
    	# EXIT or KILL functions, close the server
    	else:
    		self.sock_conn.close()

    	return closeConnection

# ||| STANDALONE TEST MODULES |||
def basic():
        
    client = wifi_client(5560)
    ConnectionClosed = False

    while not ConnectionClosed:
        message = input("Enter your message: ")
        ConnectionClosed = client.DataTxToHost(message)

    print("Socket closed..")

def protocol():

    c = client(5560, .01)

    while True:
        req = '0'
        x,y,z = c.request(req)
        print("X: " + str(x))
        print("Y: " + str(y))
        print("Z: " + str(z))

if __name__ == "__main__":
    print(sys.version)
    protocol()

