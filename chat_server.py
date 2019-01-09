import socket
import sys
import threading

# Close all client sockets when the server_socket is closed

clients_dict = {}
username_ip_dict = {}
ip_client_dict = {}

def handle_client_thread(client_connection, client_address):

	client_connected = True
	new_user = True
	username = ''

	welcome_message = "Welcome to the server... Enter your username:"
	client_connection.sendall(welcome_message.encode())

	try:

		while client_connected:

			data = client_connection.recv(1024)
			received_message = data.decode()

			if not data:
				print("Lost connection to client %s:%s unexpectedly" % (client_address[0], str(client_address[1])))
				break
			else:
				if new_user:
					username = received_message
					clients_dict[username] = client_connection
					new_user = False
					print("New user: %s" % username)
				elif received_message == 'quit':
					client_connected = False
					print("Client %s:%s has requested to close connection" % (client_address[0], str(client_address[1])))
				else:
					print("Message from %s: %s" % (username, received_message))
					valid_user = False
					for name in clients_dict.keys():
						if ('>>' + name + ':') in received_message:
							valid_user = True
							chat_message = received_message.replace('>>' + name + ':', username + ':')
							clients_dict.get(name).sendall(chat_message.encode())

					if not valid_user:
						response_message = "Not a valid message"
						client_connection.sendall(response_message.encode())

	except:
		print("An error occurred wiith client %s:%s" % (client_address[0], client_address[1]))

	finally:

		print("Closing connection with %s:%s..." % (client_address[0], str(client_address[1])))
		client_connection.close()



if __name__ == "__main__":

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_ip_address = str(socket.gethostname())
	server_port = 2223

	print("Server address: %s:%s" % (server_ip_address, str(server_port)))

	server_socket.bind((server_ip_address, server_port))

	server_socket.listen(5)

	try:

		while 1:
			print("Server is waiting for clients...")
			
			client_connection, client_address = server_socket.accept()

			print("Connected to client with address %s:%s" % (client_address[0], str(client_address[1])))

			threading.Thread(target = handle_client_thread, args = (client_connection, client_address, )).start()
	
	finally:
		print("Closing server_socket")
		server_socket.close()
		sys.exit()

