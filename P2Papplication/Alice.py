import socket
import server

# Gets the private IP address of the local machine
host_addr = socket.gethostbyname(socket.gethostname())
port = 9999
sock = server.Server.create_socket(host_addr, port= port)
sock.listen(5)

print("Alice listening to ")

peers = []

while True:
    try:
        client_conn, address = sock.accept()

        # Sends a JOIN request. All messages are formatted as MSG_TYPE, ACTUAL_MSG
        request = 'JOIN,'
        request_byte = request.encode('uft-8')
        client_conn.send(request_byte)

        response_byte = client_conn.recv(1024)
        if 'SUCCESS' in request_byte.decode('uft-8'):
            print("Become my peer")
            peers.append(address[0])

    except KeyboardInterrupt:
        print("Disconnecting...")
        break

    except:
        print("Error occurred.")

