import socket
import sys
import time

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_address = ('localhost', 10000)
print >> sys.stderr, 'Server: starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print >> sys.stderr, 'Server: waiting for a connection...'
	connection, client_address = sock.accept()

	try: 
		print >> sys.stderr, 'Server: connection from % s port %s' % client_address

		message = ""
		# Receive the data
		while True:
			data = connection.recv(16)
			time.sleep(1)
			print >> sys.stderr, 'Server: received "%s"' % data
			if data: 
				print >> sys.stderr, 'Server: sending data back to the client'
				message += data.upper()
				connection.sendall(data.upper())
			else: 
				print >> sys.stderr, 'Server: no more data from %s port %s' % client_address
				print >> sys.stderr, 'Server: complete message is %s' % message
				break
	finally:
		# Clean up the connection
		print >> sys.stderr, "Server: closing the connection"
		connection.close()
