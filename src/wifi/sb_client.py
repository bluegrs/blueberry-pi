import socket

# NOTE: Check IP address when switching over to Wi-Fi.
host = '192.168.1.168'

# NOTE: Test if this has to be the same port as the one
# 		on the server side.
port = 5560

# Socket set up for TCP packets.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
print("Connection to server was successful")

while True:
	command = input("Enter your command: ")
	
	# Decode the command ------------------
	
	# Send the EXIT request to other end
	# and exit the connection.
	if command == 'EXIT':
		s.send(str.encode(command))
		break
		
	# Send KILL command to shut down the server.
	# Same behavior on client side.
	elif command == 'KILL':
		s.send(str.encode(command))
		break
		
	# If other command, just send the command
	# and wait for the response.
	s.send(str.encode(command))
	reply = s.recv(1024)
	print(reply.decode('utf-8'))
	
s.close()
