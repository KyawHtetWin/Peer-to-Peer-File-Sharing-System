import socket
import os
import pickle
""" 
	This function sends a single specified file over the socket connection 
"""
directory = "./shared_folder"

def send_file(f_name, sock):
	with open(f_name, 'rb') as f:
		sock.sendfile(f, 0)

s = socket.socket()
s.bind(('localhost', 12345))
s.listen(5)

while True:
    client_sock, addr = s.accept()
    if "REQ" in client_sock.recv(1024).decode("utf-8"):
        # First send a list of file name
        file_names = [f_name for f_name in os.listdir(directory) if not f_name.startswith(".")]
        data = str(file_names).encode("utf-8")
        client_sock.send(data)
        # Then send each file
        for filename in file_names:
            send_file(filename, client_sock)

client_sock.close()


