import os
import re
import time
import concurrent.futures
import socket
import random
import server


''' Opens a pipe to or from Terminal to get devices on a local network by broadcasting ARP packet request and parsing 
	the result(tested on Mac) to return a list of IP address of all active devices in LAN. '''

def find_local_nodes():
    nodes = [node for node in os.popen('arp -a')]
    # Extract all instances of IP addresses found inside parantheses using
    # regular expressions
    ip_addresses = [re.search('\(([^)]+)', node).group(1) for node in nodes]
    print("All IP addresses: ")
    # print(ip_addresses)
    return ip_addresses



# Gets the private IP address of the local machine
#host_addr = socket.gethostbyname(socket.gethostname())
port = 9999
peers = []

start = time.perf_counter()
time.sleep(random.randint(1, 5))

if not peers:
    # Multi-threaded call to find_local_nodes
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(find_local_nodes)

        peers = f1.result()

# Now the peers list is filled with potential peers
for peer in peers:
    sock = server.Server.create_socket(peer, port= port)
    # Connect to those IP addresses
    try:
        sock.connect((peer, port))
    except socket.error as error_msg:
        print("Failed to connect to " + peer)
        print(error_msg)
    # Connected, and see if it's a peer trying to join
    else:
        data_byte = sock.recv(1024)
        # Receive a response and checks if the response is a request to join the network
        if data_byte:
            data_string = data_byte.decode('utf-8')  # Converts back to string
            if 'JOIN' in data_string:
                print(peer + " has joined the network!")
                success_msg = "SUCCESS"
                sock.send(success_msg.encode('utf-8'))
        # Otherwise, this node is not interested in becoming peer
        else:
            # Remove the device from the peer list
            peers.remove(peer)

sock.close()

end = time.perf_counter()

print("Total Duration: ", round(end - start, 2), " seconds")









