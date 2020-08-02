import socket
import threading
import sys
import time
import random

class Server:
    connections = []   # Stores all the socket object of the peer
    peers = []         # Stores all the peers' IP address connected to server

    def __init__(self):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        except socket.error as error_msg:
            print("Socket Creation Error: " + str(error_msg))
        
        try:
            sock.bind(('', 9999))
            sock.listen(5)

        except socket.error as error_msg:
            print("Socket Binding Error: " + str(error_msg) + "\nRetrying...")
        
        
        print("Server running...")

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()

            self.connections.append(c)
            self.peers.append(a[0]) 

            print(str(a[0]) + ':' + str(a[1]), " connected.")
            # Update ohter peers if someone has been connected
            self.send_peers()


    def handler(c, a):

        while True:
            data = c.recv(1024)

            for connection in self.connections:
                connection.send(data)

            if not data:
                print(str(a[0]) + ':' + str(a[1]), " disconnected.")

                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                # Update the peers if someone has disconnected
                self.send_peers()
                break



    def send_peers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))

class Client:

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 9999))

        iThread = threading.Thread(target=self.send_msg, args=(sock,))
        iThread.daemon = True
        iThread.start()

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
    peers = ['127.0.0.1']
    

while True:
    try:
        print("Trying to connect...")
        time.sleep(random.randint(1, 5))

        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Couldn't start the srever...")

    except KeyboardInterrupt:
        sys.exit(0)

