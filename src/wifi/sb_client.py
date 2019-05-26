import socket
import sys

# NOTE: Check IP address when switching over to Wi-Fi.
# NOTE: Test if this has to be the same port as the one
# 		on the server side.
def DefineSocketInfo():
	host = '192.168.1.29'
	port = 5560
	return host, port

# DESC: Set up the client-side socket for TCP packets
# RETURNS: socket.socket
def SetupClient(socket_data_tuple):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(socket_data_tuple)
	print("Connection to server was successful")
	return sock

# DESC: Decodes the command to be sent to the server
#		and returns the response.
# RETURNS: boolean to break or not
def DataTransfer(command):
	
	# Determine if the data transfer should continue or 
	# if the socket should close down
	exit_loop = False
	
	# Decode the command ------------------
	# Send the EXIT request to other end
	# and exit the connection.
	if command == 'EXIT':
		s.send(str.encode(command))
		exit_loop = True
		
	# Send KILL command to shut down the server.
	# Same behavior on client side.
	elif command == 'KILL':
		s.send(str.encode(command))
		exit_loop = True
		
	# If other command, just send the command
	# and wait for the response.
	s.send(str.encode(command))
	if not exit_loop:
		reply = s.recv(1024)
		print(reply.decode('utf-8'))
	
	return exit_loop

# ============================ STANDALONE ================================
if __name__ == "__main__":

	print(sys.version)
	sock_data = DefineSocketInfo()
	exit_loop = False # for infinite data transfer once connection is made
	
	# After host and port are determined, 
	s = SetupClient(sock_data)
		
	while not exit_loop:
		instruction = input("Enter your command: ")
		exit_loop = DataTransfer(instruction)
		print(str(exit_loop))
	
	# If the loop has exited, close the socket.
	s.close()
	print("SOCKET CLOSED..")
