import socket
import sys
import _thread

def client_thread(conn, client_address):

	welcome_message = "Connected to the server... Enter a message: \n"
	conn.sendall(welcome_message.encode())

	try:

		while True:
			raw_data = conn.recv(1024)
			received_message = raw_data.decode().rstrip()

			print("Received: " + received_message)

			if not raw_data:
				print("Connection with " + client_address[0] + ": " + str(client_address[1]) + " was closed unexpectedly")
				break
			elif received_message == 'quit':
				print("Closing connection with client " + client_address[0] + ": " + str(client_address[1]))
				break
			else: 
				reply_message = received_message.upper() + '\n'
				conn.sendall(reply_message.encode())
	finally:

		conn.close()


host = 'localhost'
port = 8888

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket created")

# Bind socket to a port
try:
	s.bind((host, port))
except socket.error:
	print("Binding Error")
	sys.exit()

# Listen 
s.listen(10)

while True:

	print("Server is listening for clients...")
	conn, client_address = s.accept()

	print("Connected with client " + client_address[0] + ": " + str(client_address[1]))

	_thread.start_new_thread(client_thread, (conn, client_address))