"""
TESTED MODULE: Represents an individual peer that is looping to take the role of the
               client and then server until interrupted by keyboard from users.
"""


import time
import random
import sys
import server
import client
import hashlib
import os

# The shared folder containing all the files shared by all peers in the network should share
DIRECTORY = "./shared_folder"

PORT = 5000

class Peer:
    # Loopback address (for demo purpose)
    # The final program should store a list of known peers
    peers = ['127.0.0.1']

    def __init__(self):
        # A list of key of all the files in shared_folder of this peer (positional dependent)
        self.all_files = []
        self.peers = []

    # TODO:Implements a hash table as follows: Hashed Key of File ===> [peer1, peer2, ...]

    """ Given a filename, a peer hash the file using sha3-256 algorithm and returns 
        a resulting hexdecimal hashed key in string  """

    def hash_file(self, f_name, block_size=6*1024):
        # Creates a hash object
        file_hash = hashlib.sha3_256()
        # Open file to read its bytes
        with open(f_name, 'rb') as f:
            while True:
                data = f.read(block_size)
                # Once finished reading the file, quit
                if not data:
                    break
                # Update the hash if there is data
                file_hash.update(data)
        return file_hash.hexdigest()

    """ Given a directory, it hashes all the files inside it and returns a list of hashed key """

    def update_all_files(self, directory):
        keys = [] # Stores all the hashed-values of files
        # Loops over the files in directory
        for filename in os.listdir(directory):
            # Ignoring the file (.DS_Store)
            if not filename.startswith('.'):
                # Hash the file
                keys.append(self.hash_file(filename))

        return keys

def main():

    while True:
        try:
            print("Trying to connect...")
            # Randomly sleeps before becoming a peer
            time.sleep(random.randint(1, 5))

            for peer in Peer.peers:
                # Becomes a Client
                try:
                    client.Client(peer, PORT)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                print("="*40)
                # Becomes a Server
                try:
                    # Gets the private IP address of the local machine
                    # address = socket.gethostbyname(socket.gethostname())
                    server.Server(PORT, address='127.0.0.1')
                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as e:
                    print("Failed to start server")
                    print(e)
                    break

        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()