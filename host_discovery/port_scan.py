
import socket

# Target Host, www.example.com
t_host = str(input("Enter the host to be scanned: "))
# Resolve t_host to IPv4 address
t_ip = socket.gethostbyname(t_host)

print(t_ip)  # Print the IP address

while True:
    # Enter the port to be scanned
    t_port = int(input("Enter the port: "))

    try:
        sock = socket.socket()
        res = sock.connect((t_ip, t_port))
        print("Port {}: Open".format(t_port))
        sock.close()

    except:
        print("Port {}: Closed".format(t_port))

print("Port Scanning complete")