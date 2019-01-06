import socket
import sys

# Create a socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Failed to connect")
	sys.exit()

print("Socket Created")

host = "www.google.com"
port = 80

try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("Host name could not be resolved")
	sys.exit()

print("IP Address for " + host + ": " + remote_ip)

server_address = (remote_ip, port)

# Connect socket to the server's port
s.connect(server_address)
print("Socket connected to " + host + " using IP " + remote_ip)

message = "GET / HTTP/1.1\r\n\r\n"

try:
	s.sendall(message.encode())
except socket.error:
	print("Did not send successfully")
	sys.exit()

print("Message sent successfully")

reply = s.recv(4096)

print(reply.decode())

s.close()



