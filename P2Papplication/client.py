"""
TESTED MODULE: Client sends an update for files when run and appropriately handles
               the different responses that can be received from servers.

"""

import socket
import random
import sys
from simplep2p import Peer

class Client:
    """ Constructor: Initializes everything and run the client"""

    def __init__(self, address, port):
        print("\nClient running...")
        # Creates a socket to send and receive information
        self.sock = self.create_socket(address=address, port=port)

        if self.sock:
            # print("Client Socket created successfully...")
            # Connect to specified address and port
            self.sock.connect((address, port))

            try:
                self.send_fupdate_req()
                while True:
                    resp_byte = self.sock.recv(1024)
                    # Receives response from server
                    if resp_byte:
                        # Decode the response back into string
                        resp = resp_byte.decode("utf-8")

                        """ Handles different responses the server can send """
                        # Server sends a peer list to update
                        if "PLIST" in resp:
                            print("\nReceived peer list:")

                            # The list of peer can be obtained without the message type
                            # identifier(first element) & last extra element of the response string
                            Peer.peers = resp.split(",")[1:-1]
                            print(Peer.peers)

                        # Server has sent a response of the file
                        else:
                            # Just print the response
                            print("\nReceived - " + resp)

                    # No response from server
                    else:
                        print("\nNo response from server")
                        self.sock.close()
                        break
            # Keyboard Interrupt to quit client
            except KeyboardInterrupt:
                self.sock.close()  # Closes the socket
                self.send_pexit_req()  # Send the PEXIT request to server
                print("Exiting as Client")

        else:
            print("Exiting as Client")
            sys.exit()

    """ This method handles the creation of a socket and displays appropriate errors if they happened. If
        successful, it returns a socket object. """

    def create_socket(self):
        try:
            # Creates a socket to communicate using TCP/IPv4
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Configure to make the port reusable immediately
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s
            # Catches any error when creating a socket
        except socket.error as error_msg:
            print("Socket Creation Error: " + str(error_msg))
            return None

    """ Simulates sending of a request for a file """

    def send_fupdate_req(self):
        msg = "File: " + str(random.randint(1, 20))
        print("Requesting " + msg)
        # All requests should be sent in the format REQUESTTYPE, MESSAGE
        send_req = "FUPDATE," + msg + ","
        send_req_byte = send_req.encode("utf-8")
        self.sock.send(send_req_byte)

    """ Send a request to disconnect """

    def send_pexit_req(self):
        print("\nDisconnecting from server")
        exit_req = "PEXIT,"
        exit_req_byte = exit_req.encode('utf-8')
        self.sock.send(exit_req_byte)
        # Quit this instance
        sys.exit()




