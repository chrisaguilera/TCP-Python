import socket
import sys
import time

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >> sys.stderr, 'Client: connecting to %s port %s' % server_address
sock.connect(server_address)

try:
	# Send data
	message = 'This is a message. It will be echoed back from the server.'
	print >> sys.stderr, 'Client: sending "%s"' % message
	sock.sendall(message)

	# time.sleep(10)

	# Wait for the response
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected: 
		data = sock.recv(16)
		amount_received += len(data)
		print >> sys.stderr, 'Client: received "%s"' % data

finally:
	print >> sys.stderr, 'Client: closing the socket in 10 seconds'
	time.sleep(10)
	sock.close()