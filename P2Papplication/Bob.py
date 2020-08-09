"""
TESTING MODULE: In trying to discover potential peers, Bob probes the LAN by sending
                out ARP request to get a list of IP address of all active devices.
                Bob connects to those IP addresses hoping that a peer already in the
                network(Alice) will send a JOIN message. Bob responds with acknowledgement or
                SUCCESS message, becoming Alice's peer.

"""



import os
import re
import time
import concurrent.futures
import socket
import random


''' Opens a pipe to or from Terminal to get devices on a local network by broadcasting ARP packet request and parsing 
	the result(tested on Mac) to return a list of IP address of all active devices in LAN. '''

def find_local_nodes():
    nodes = [node for node in os.popen('arp -a')]
    # Extract all instances of IP addresses found inside parantheses using
    # regular expressions
    ip_addresses = [re.search('\(([^)]+)', node).group(1) for node in nodes]
    print("All IP addresses found: ")
    # print(ip_addresses)
    return ip_addresses

''' Scan a given IP address for a given port'''
def port_scanner(s, target_ip, target_port):
    try:
        s.connect((target_ip, target_port))
        return True
    except:
        return False

''' Scan all open ports on a target ip '''
def get_open_port(ip):
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(1, 1024):
        if port_scanner(S, ip, port):
            print("Port " + str(port) + " Open")
    S.close()


""" This method handles the creation of a socket and displays appropriate errors if they happened. If
    successful, it returns a socket object. """

def create_socket(address, port):
    try:
        # Creates a socket to communicate using TCP/IPv4
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configure to make the port reusable immediately
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Catches any error when creating a socket
    except socket.error as error_msg:
        print("Socket Creation Error: " + str(error_msg))

    try:
        # Binds the host and port to the socket
        s.bind((address, port))
        # Listen to computers making connection to the socket
        s.listen(5)
        return s

        # Catches any error when binding the socket
    except socket.error as error_msg:
        print("\nSocket Binding Error: " + str(error_msg))
        print("For IP address ", address)
        return None


# Gets the private IP address of the local machine
host_addr = socket.gethostbyname(socket.gethostname())
port = 64255
peers = []
start = time.perf_counter()
time.sleep(random.randint(1, 5))
print("Bob scanning LAN...")

if not peers:
    # Multi-threaded call to find_local_nodes
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(find_local_nodes)

        peers = f1.result()

print(peers)


# Now the peers list is filled with potential peers
for peer in peers:
    sock = create_socket(peer, port= port)

    if sock:
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
                    print("Found " + peer)
                    success_msg = "SUCCESS"
                    sock.send(success_msg.encode('utf-8'))
            # Otherwise, this node is not interested in becoming peer
            else:
                # Remove the device from the peer list
                peers.remove(peer)

        sock.close()

end = time.perf_counter()

print("Total Duration: ", round(end - start, 2), " seconds")









