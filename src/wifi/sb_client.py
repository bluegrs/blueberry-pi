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

TODO:
~ The class needs a function to adjust the host IPv4 address.
~ The data being sent should be read from some external resource
	such as a FIFO.
'''

# =====================================================
# =====================================================
# ==											     ==
# ==			   IMPORT DEPENDENCIES
# ==											     ==
# =====================================================
# =====================================================
import socket
import sys

class wifi_client:
	
	def __init__(self, port):
		
		self.host = '192.168.1.26'
		self.port = port
		self.sock_conn = None
		
		# Setup the socket from the port number provided
		self.__SetupClient()

	# =====================================================
	# =====================================================
	# ==											     ==
	# ==			   PRIVATE METHODS
	# ==											     ==
	# =====================================================
	# =====================================================
	
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
		
	# =====================================================
	# =====================================================
	# ==											     ==
	# ==			     PUBLIC METHODS
	# ==											     ==
	# =====================================================
	# =====================================================

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

# =====================================================
# =====================================================
# ==											     ==
# ==			     STAND ALONE
# ==											     ==
# =====================================================
# =====================================================
if __name__ == "__main__":

	print(sys.version)

	client = wifi_client(5560)
	ConnectionClosed = False
		
	while not ConnectionClosed:
		message = input("Enter your message: ")
		ConnectionClosed = client.DataTxToHost(message)
	
	print("Socket closed..")
