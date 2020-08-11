import socket
import pickle

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

msg = "FREQ"

s.send(msg.encode('utf-8'))
# First receive a list of file names
data = s.recv(1024)
filenames = eval(data)
print(filenames)

read_file(filenames[0], s)
print("Successfully get the file")

'''
read_file(f_name= filename, sock= s)

print("Successfully get the file")
'''

s.close()


