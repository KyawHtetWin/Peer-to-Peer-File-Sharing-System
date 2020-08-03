import time
import random
import server
import client
import sys

PORT = 9999

class Peer:
    # Loopback address
    peers = ['127.0.0.1']

def main():
    while True:
        try:
            print("Trying to connect...")
            # Randomly sleeps before becoming a peer
            time.sleep(random.randint(1, 5))

            for peer in Peer.peers:
                try:
                    client.Client(peer, PORT)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                try:
                    server.Server(PORT)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print("Failed to start server")

        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()