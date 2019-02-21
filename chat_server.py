import socket
import sys
import threading

# Close all client sockets when the server_socket is closed

client_connection_list = []
username_list = []
client_dict = {}
chats = []

def send_all_clients(message):
	try:
		for c_connection in client_connection_list:
			c_connection.sendall(message.encode())
	except:
		print("An error occurred trying to send message to all client connections")


def handle_client_thread(client_connection, client_address):

	username = ""
	friend_username = ""
	client_connected = True

	welcome_message = ''.join(username_list)

	client_connection.sendall(welcome_message.encode())

	try:

		while client_connected:

			data = client_connection.recv(1024)
			received_message = data.decode()

			if not data:
				print("Lost connection to client %s:%s unexpectedly" % (client_address[0], str(client_address[1])))
				break
			else:
				print("Message from %s:%s: %s" % (client_address[0], str(client_address[1]), received_message))
				split_message = received_message.split("::")

				if split_message[0] == "joinLobby":

					# Remove trailing whitespace from message
					username = split_message[1].rstrip()

					# Add username to list and dict
					username_list.append(username)
					client_dict[username] = client_connection
					print(client_dict)

					# Convert username list to string
					username_list_string = "::".join(username_list)
					# Notify all clients of new user
					message = "newUser::" + username_list_string
					send_all_clients(message)

				# elif split_message[0] == "requestUsers":
				# 	username_list_string = "::".join(username_list)
				# 	message = "users::" + username_list_string
				# 	client_connection.sendall(message.encode())

				elif split_message[0] == "chatRequestWith":
					
					# Remove trailing whitespace from message
					friend_username = split_message[1].rstrip()

					# Notify friend of chat request
					message = "chatRequestFrom::%s" % username
					friend_connection = client_dict.get(friend_username)
					friend_connection.sendall(message.encode())

				elif split_message[0] == "acceptChatRequest":
					
					friend_username = split_message[1]

					# Begin chat
					message = "beginChat::%s::%s" % (friend_username, username)

					# Send to friend
					friend_connection = client_dict.get(friend_username)
					friend_connection.sendall(message.encode())

					# Send to self
					client_connection.sendall(message.encode())

				elif split_message[0] == "sendNewMessage":

					message = "newMessage::%s::%s" % (username, split_message[3])

					# Send to friend
					if friend_username == split_message[2]:
						friend_connection = client_dict.get(split_message[2])
						friend_connection.sendall(message.encode())
					else:
						print("Friend username is incorrect")
				
				else:
					print(split_message)

	except:
		print("An error occurred wiith client %s:%s" % (client_address[0], client_address[1]))

	finally:

		print("Closing connection with %s:%s..." % (client_address[0], str(client_address[1])))
		client_connection.close()



if __name__ == "__main__":

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# server_ip_address = str(socket.gethostname())
	server_ip_address = "0.0.0.0"
	server_port = 2223

	print("Server address: %s:%s" % (server_ip_address, str(server_port)))

	server_socket.bind((server_ip_address, server_port))

	server_socket.listen(5)

	try:

		while 1:
			print("Server is waiting for clients...")
			
			client_connection, client_address = server_socket.accept()

			print("Connected to client with address %s:%s" % (client_address[0], str(client_address[1])))

			client_connection_list.append(client_connection)

			threading.Thread(target = handle_client_thread, args = (client_connection, client_address, )).start()
	
	finally:
		print("Closing server_socket")
		server_socket.close()
		sys.exit()

