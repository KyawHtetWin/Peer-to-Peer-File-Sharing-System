import socket 
import tqdm 
import os

BUFFER_SIZE = 4096 # No. of Bytes to send each time

host = "" 
port = 5000

# File to send
filename = "foo.rtf"

# Gets the file size
filesize = os.path.getsize(filename)

s = socket.socket()

print("Connecting to " + host + ":" + str(port))
s.connect((host, port))
print("Connected")

msg = filename + "," + str(filesize)
msg_byte = msg.encode("utf-8")
# Send the filename and filesize
s.send(msg_byte)

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", 
				unit="B", unit_scale=True, unit_divisor=1024)

with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
       
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the socket
s.close()


