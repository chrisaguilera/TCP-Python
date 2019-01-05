import socket
import sys

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

s.connect(server_address)

print("Socket connected to " + host + " using IP " + remote_ip)



