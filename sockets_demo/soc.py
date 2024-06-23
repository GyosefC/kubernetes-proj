import socket


def start_socket_listener(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Listening for connections on {host}:{port}...")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receive and print data from the client
        data = client_socket.recv(1024)
        print(f"Received data: {data.decode('utf-8')}")

        # Send a response back to the client
        response = "Hello from the client!\r\n"
        client_socket.send(response.encode('utf-8'))

        # Close the connection with the client
        client_socket.close()


if __name__ == "__main__":
    # Set the host and port to listen on
    host = "127.0.0.1"
    port = 12345

    # Start the socket listener
    start_socket_listener(host, port)
