import socket 

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

filename = 'received_file.py'

read_file(f_name= filename, sock= s)

print("Successfully get the file")

s.close()


