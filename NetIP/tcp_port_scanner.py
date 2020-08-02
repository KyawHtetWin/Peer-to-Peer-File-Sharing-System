import socket
from datetime import datetime
import threading

from queue import Queue

# Used to prevent double entries from shared variables
print_lock = threading.Lock()

ip = input("Enter Host Address to Scan: ")

# Translate a host name to IPv4 address format
# ip = socket.gethostbyname(host)

print("\nScanning the host : ", ip, "\n")

t1 = datetime.now()


# Code for port scanning
def scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))

        if result == 0:
            print("Port " + str(port) + ": Open")
        else:
            print("Port " + str(port) + ": Closed")

        sock.close()

    except:
        pass


t2 = datetime.now()

total = t2 - t1
print("Total Scanning Time: ", total)


# Create a threader function
def threader():
    while True:
        worker = q.get()  # Get worker from the queue
        scan(worker)  # Run the job with the available worker in queue
        q.task_done()  # Complete with the job


# Create a queue
q = Queue()

# The number of thread(s)
for x in range(60):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1, 100):
    q.put(worker)

# Thread will join after thread termination
q.join()



