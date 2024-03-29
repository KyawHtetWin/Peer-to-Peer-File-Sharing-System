
from constants import *
from client import *
from server import *


"""
    This class will take care of converting client to server
"""
class p2p:
    # make ourself the default peer
    peers = ['127.0.0.1']


def main():
    # if the server breks we try to make a client a new server
    #msg = convert()
    while True:
        try:
            print("-" * 21 + "Trying to connect" + "-" * 21)
            # sleep a random time between 1 -5 seconds
            time.sleep(randint(RAND_TIME_START,RAND_TIME_END))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass


                # become the server
                try:
                    msg = "THIS IS SERVER"
                    msg = str.encode(msg)
                    server = Server(msg)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)

if __name__ == "__main__":
    main()
