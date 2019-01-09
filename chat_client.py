import socket
import sys
import threading
import errno

client_running = True

def listening_thread(client_socket):

	global client_running

	while client_running:
		
		try:

			data = client_socket.recv(1024)

			if not data:
				print("Lost connection to server")
				client_running = False

			else:
				received_message = data.decode()
				print('<<' + received_message)

		except:
			print("Disconnected from server")
			client_running = False

if __name__ == "__main__":

	client_ip_address = str(socket.gethostname())

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_ip_address = '192.168.0.13'
	server_port = 2223

	print("Connecting to server %s:%s..." % (server_ip_address, str(server_port)))

	# Exit the program if cannot connect
	try:
		client_socket.connect((server_ip_address, server_port))

	except socket.error:
		print("Connection refused")
		sys.exit()

	threading.Thread(target = listening_thread, args = (client_socket, )).start()

	while client_running:

		client_input = input()

		try:
			if client_input == 'quit':

				print("Sending 'quit' message to server")
				client_socket.sendall(client_input.encode())

				client_running = False

			else:
				client_socket.sendall(client_input.encode())

		except IOError as e:
			if e.errno == errno.EPIPE:
				print("EPIPE Error")
			break

		except socket.error as e:
			print("Socket Error")

			break

	print("Closing socket from main_thread")
	client_socket.close()
