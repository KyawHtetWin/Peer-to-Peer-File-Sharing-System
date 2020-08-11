"""
TESTED MODULE: Multithreaded server that can handle multiple clients. One thread handles
               all the incoming requests from clients while another thread dispatches
               the request to be handle by appropriate functions based on the type of
               of request made at the server.
"""

import threading
import socket

class Server:
    """  Constructor: Initializes everything and starts running the server. """

    def __init__(self, port, address=""):
        print("\nServer running...")

        self.all_conn = []  # Stores all the socket objects of neighbor
        self.all_neighbor = []  # Stores all the neighbors
        # Creates server socket
        self.sock = self.create_socket(address=address, port=port)

        # A dictonary storing the corresponding function of the types of requests that a client can make
        self.handlers = {
            'FUPDATE': self.handle_file_update,
            'PEXIT': self.handle_peer_exit
        }

        while True:
            try:
                if self.sock:
                    #print("Server Socket created successfully...")
                    # Start accepting connections from other nodes
                    client_sock, client_addr = self.sock.accept()

                    # Append that client to known connection & neighbor list
                    self.all_conn.append(client_sock)
                    self.all_neighbor.append(client_addr)

                    # Start a new thread to handle the actual client request
                    t = threading.Thread(target=self.req_dispatcher, args=(client_sock, client_addr))
                    t.daemon = True
                    t.start()
                    # See how many threads (connections) are active
                    #print("Active Connections: " + str(threading.activeCount()-1))

                    print("Connection established! " + str(client_addr))

                    # Send the peer list to all neighbors whenever a new node has been connected
                    self.send_peerList()
                # Socket not created properly, so quit the server
                else:
                    break

            # The user wants to exits the server
            except KeyboardInterrupt:
                print("\nExiting the server")
                self.sock.close()
                client_sock.close()
                #sys.exit()
                break

            except:
                self.sock.close()
                client_sock.close()
                print("Error accepting connections")
                break


    """ Call the appropriate handler function based on the kinds of request from peer """

    def req_dispatcher(self, client_sock, client_addr):

        # while True:
        # Receives the request from client
        data_byte = client_sock.recv(1024)

        if data_byte:
            data_string = data_byte.decode('utf-8')  # Converts back to string
            '''
            Request are always sent in following comma-separated format:
                    REQUEST_TYPE, ACTUAL MESSAGE
            Pass client_sock, client_addr, and the acutal message as a list to call correct handlers
            '''
            self.handlers[data_string.split(",")[0]](client_sock, client_addr, data_string.split(",")[1:])

            # Close the socket connection
            #client_sock.close()
        else:
            print("No data received")
            # break

    """ This method handles the exit of a node from the network """

    def handle_peer_exit(self, sock, addr, data):
        # Remove the peer from the list
        self.all_conn.remove(sock)
        self.all_neighbor.remove(addr)
        print("Peer " + str(addr) + " Exited")
        # Give updates of the exit to all other the neighbors
        self.send_peerList()

    """ This method simulates the sharing of the file that is being requested to all the known peers. The data
        is passed as the list """

    def handle_file_update(self, sock, addr, data):
        # TODO: Lookup the file in hash table, if found, respond, else ask neighbors for file (Flooding)
        print("Sending the requested " + data[0] + ' to all client(s)')
        response = "Requested " + data[0]
        # Encode the respond into bytes
        res_byte = response.encode("utf-8")
        for conn in self.all_conn:
            conn.send(res_byte)

    """ This method handles the creation of a socket and displays appropriate errors if they happened. If
        successful, it returns a socket object. """

    def create_socket(self, address, port):
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

    """ Sends the list of peers to all the known peers"""

    def send_peerList(self):
        # print("Inside send_peerList")
        p_list = ""  # A comma-separated string of a list of all peers IP address
        for neighbor in self.all_neighbor:
            p_list += str(neighbor[0]) + ','

        # Appends the message identifier at the beginning
        p_list = "PLIST," + p_list
        #print("p_list: " + p_list)

        # Converts the string message to bytes to send over socket connection
        p_list_byte = p_list.encode('utf-8')

        # Sends the peerList to all peers
        for conn in self.all_conn:
            conn.send(p_list_byte)


