import socket
import threading

clients = {}

def broadcast_message(sender: socket, message: bytes) -> None:
    for client in list(clients.keys()):
        # Don't send the message to the sender because it already has it in its terminal
        if clients[client]["socket"] != sender:
            try:
                clients[client]["socket"].sendall(message)
                print(
                    f"[THREAD {threading.get_native_id()}] Message \"{message.decode()}\" sent to {client[0]}:{client[1]} !")
            # If the client has disconnected, join the thread and remove it from the clients dictionary
            except:
                print(f"[THREAD {threading.get_native_id()}] Client {client[0]}:{client[1]} has disconnected, joining thread...", end="")
                clients[client]["thread"].join()
                clients.pop(client)
                print("\t[DONE]")

def handle_client(client_sock: socket, client_info: tuple[str, int]) -> None:
    while True:
        message = client_sock.recv(1024)
        if message:
            print(f"[THREAD {threading.get_native_id()}] {client_info[0]}:{client_info[1]} sent: {message.decode()}")
            print(f"[THREAD {threading.get_native_id()}] Sending message to all clients...")
            broadcast_message(client_sock, message)
        # message will be empty if the client shut down its socket
        # We can then properly close the socket
        # NOTE: We can't join the thread here because it's the thread we are in right now
        else:
            print(f"[THREAD {threading.get_native_id()}] Client {client_info[0]}:{client_info[1]} has disconnected")
            print(f"[THREAD {threading.get_native_id()}] Closing socket of client {client_info[0]}:{client_info[1]}...", end="")
            clients[client_info]["socket"].close()
            print("\t [DONE]")
            return


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 3011

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Chat server listening on {HOST}:{PORT}")
        try:
            while True:
                # client_address is a tuple with the format (IP,port)
                client_socket, client_address = server.accept()
                print(f"Received connection from {client_address[0]}:{client_address[1]}, starting dedicated thread...", end="")
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                thread.start()
                clients[client_address] = {"socket": client_socket, "thread": thread}
                print("\t[DONE]")
        except KeyboardInterrupt:
            print("Stopping chat server (Ctrl+C)...")
            server.shutdown(socket.SHUT_RDWR)
            server.close()

            # Shut down all client sockets and join all threads
            for client in list(clients.keys()):
                # Some clients in the list might have already disconnected, but their thread might not have been cleaned up yet
                if clients[client]["socket"].fileno() != -1:
                    print(f"Shutting down socket for client {client[0]}:{client[1]}...", end="")
                    clients[client]["socket"].shutdown(socket.SHUT_RDWR)
                    # When the socket is shut down, the thread executing handle_client() will close the socket,
                    # causing the execution of the thread to end
                    # We can now join the thread safely
                    print("\t[DONE]")
                clients[client]["thread"].join()
