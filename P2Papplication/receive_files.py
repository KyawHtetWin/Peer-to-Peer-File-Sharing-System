"""
TESTING MODULE: This purpose of this module is to accept all the files that send_files
                module sent. WORK IN PROGRESS.
"""

import socket

''' This function accepts a single file  and write the file to the 
    current directory'''

def read_file(f_name, sock):
	with open(f_name, 'wb') as f:
		while True:
			data = sock.recv(CHUNK_SIZE)

			if not data:
				break

			f.write(data)

CHUNK_SIZE = 8*1024

s = socket.socket()
s.connect(('localhost', 12345))

# Send a request for file to server
msg = "FREQ"
s.send(msg.encode('utf-8'))

# Receive a list of file names
data = s.recv(1024)
filenames = eval(data)
print(filenames)
# Get the file
read_file(filenames[0], s)
print("Successfully get the file")

s.close()


