import socket
import sys
import threading

def listening_thread(client_socket):
	try:
		while 1:
			data = client_socket.recv(1024)
			if not data:
				print("Lost connection to server")
				break
			
			received_message = data.decode()
			print('Server: ' + received_message)
	finally:
		print("Closing socket from listening_thread")
		client_socket.close()


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

	try:

		threading.Thread(target = listening_thread, args = (client_socket, )).start()

		while 1:
			client_input = input()
			if client_input == 'quit':
				quit_message = "Client %s requesting to close connection" % client_ip_address
				client_socket.sendall(quit_message.encode())
				break

			client_socket.sendall(client_input.encode())
	
	except IOError as e:
		if e.errno == errno.EPIPE:
			print("EPIPE Error")

	except socket.error as e:
		print("Socket Error")

	finally:
		print("Closing socket from main_thread")
		client_socket.close()