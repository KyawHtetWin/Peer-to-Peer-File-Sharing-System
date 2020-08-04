import socket

""" 
	This function sends a single specified file over the socket connection 
"""
def send_file(f_name, sock):
	with open(f_name, 'rb') as f:
		sock. sendfile(f, 0)
'''
s = socket.socket()
s.bind(('localhost', 12345))
s.listen(5)

filename = 'hello_world.py'

while True:
	client_sock, addr = s.accept()
	send_file(filename, client_sock)
	client_sock.close()
'''

import os

directory = "./shared_folder"

for filename in os.listdir(directory):
	if not filename.startswith('.'):
		print(filename)

