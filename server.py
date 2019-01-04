import socket
import sys

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
		print >> sys.stderr, 'Server: connection from', client_address

		# Receive the data
		while True:
			data = connection.recv(16)
			print >> sys.stderr, 'received "%s"' % data
			if data: 
				print >> sys.stderr, 'Server: sending data back to the client'
				connection.sendall(data)
			else: 
				print >> sys.stderr, 'Server: no more data from %s' % client_address
				break
	finally:
		# Clean up the connection
		connection.close()
