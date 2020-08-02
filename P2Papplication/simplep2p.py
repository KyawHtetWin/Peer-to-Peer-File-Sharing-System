import socket
import threading
import sys
import time
import random

PORT = 9999

class Server:
    # A list of socket objects that are connected to the Server
    connections = []
    # A list of IP address that corresponds to the socket in connections list
    ip_addr = []

    """
    Constructor: Creates a socket and start listening for connections. For incoming connections, 
    start a separate thread to handle them.
    """
    def __init__(self, port, address=''):
        try:
            # Creates a socket to communicate using TCP/IPv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Configure to make the port reusable immediately
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Catches any error when creating a socket
        except socket.error as error_msg:
            print("Socket Creation Error: " + str(error_msg))

        try:
            # Binds the host and port to the socket
            sock.bind((address, port))
            # Listen to computers making connection to the socket
            sock.listen(5)
        # Catches any error when binding the socket
        except socket.error as error_msg:
            print("Socket Binding Error: " + str(error_msg))

        print("Server running...")

        while True:
            try:
                # Start accepting connections from other nodes
                client_sock, client_addr = sock.accept()

                thread = threading.Thread(target=self.handler, args=(client_sock, client_addr))
                thread.daemon = True
                thread.start()

                # Append that client to known connection & address list
                self.connections.append(client_sock)
                self.ip_addr.append(client_addr[0])

                print("Connection established! IP: " + str(client_addr[0]))
                # Update other peers if someone has been connected
                self.send_peers()

            except:
                print("Error accepting connections")

    def handler(self, client_sock, client_addr):

        while True:
            data = client_sock.recv(1024)

            for connection in self.connections:
                connection.send(data)

            if not data:
                print(str(client_addr[0]) + ':' + str(client_addr[1]), " disconnected.")

                self.connections.remove(client_sock)
                self.ip_addr.remove(client_addr[0])
                client_sock.close()
                # Update the peers if someone has disconnected
                self.send_peers()
                break

    def send_peers(self):
        p = ""
        for peer in self.ip_addr:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))


class Client:

    def __init__(self, address, port):

        try:
            # Creates a socket to communicate using TCP/IPv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Configure to make the port reusable immediately
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Catches any error when creating a socket
        except socket.error as error_msg:
            print("Socket Creation Error: " + str(error_msg))

        sock.connect((address, port))

        thread = threading.Thread(target=self.send_msg, args=(sock,))
        thread.daemon = True
        thread.start()

        while True:
            data = sock.recv(1024)

            if not data:
                break

            if data[0:1] == b'\x11':
                print("Got peers")
                self.update_peers(data[1:])

            else:
                print(str(data, 'utf-8'))

    def send_msg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def update_peers(self, peer_data):
        p2p.peers = str(peer_data, 'utf-8').split(",")[:-1]


class p2p:
    # Loopback address to start as a default client
    peers = ['127.0.0.1']


def main():
    while True:
        try:
            print("Trying to connect...")
            # Randomly sleeps before becoming a peer
            time.sleep(random.randint(1, 5))

            for peer in p2p.peers:
                try:
                    Client(peer, PORT)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                try:
                    Server(PORT)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print("Failed to start server")

        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
