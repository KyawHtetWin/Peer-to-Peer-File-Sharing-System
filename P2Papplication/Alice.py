"""
TESTING MODULE: When Alice receives an incoming TCP connection from Bob, it will
                send out JOIN response to Bob to see if Bob wants to join the
                p2p network. If Bob responds with SUCCESS, then, Bob becomes
                Alice's peer.
"""


import socket

# Simply creates socket
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
        print("Another peer already running as server\n")
        return None


# Gets the private IP address of the local machine
host_addr = socket.gethostbyname(socket.gethostname())
port = 9999
sock = create_socket(address=host_addr, port= port)
sock.listen(5)

print("Alice listening on (" + host_addr +"," + str(port) + ")")

peers = []

while True:
    try:
        client_conn, address = sock.accept()

        # Sends a JOIN request. All messages are formatted as MSG_TYPE, ACTUAL_MSG
        request = 'JOIN,'
        request_byte = request.encode('uft-8')
        client_conn.send(request_byte)

        response_byte = client_conn.recv(1024)
        # Receives SUCCESS response for JOIN message, so add the node to become peer
        if 'SUCCESS' in request_byte.decode('uft-8'):
            print("Become my peer")
            peers.append(address[0])

    except KeyboardInterrupt:
        print("Disconnecting...")
        break

    except:
        print("Error occurred.")

