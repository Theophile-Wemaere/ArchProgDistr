import select
import socket
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Missing arguments: please use format ./chat-client.py <HOST> <PORT> <PSEUDO>")
        exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    PSEUDO = sys.argv[3]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        try:
            server.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT} !")
            while True:
                # If the server socket's file descriptor is -1, it means that the socket has been shut down (connection closed by the server)
                if server.fileno() == -1:
                    print("\nConnection closed by the server.")
                    break

                sockets = [sys.stdin, server]
                readable_sockets, writable_sockets, error_sockets = select.select(sockets, [], [])

                for sock in readable_sockets:
                    # If the readable socket is the server's socket, there is an incoming message ready to be read
                    if sock == server:
                            message = sock.recv(1024)
                            if message:
                                print(message.decode())
                            else:
                                server.close()
                                break
                    # Otherwise, display a prompt to write a message
                    else:
                        message = input()
                        server.sendall(f"[{PSEUDO}] {message}".encode())
        except KeyboardInterrupt:
            print("\nDisconnected (Ctrl+C)")
            server.shutdown(socket.SHUT_RDWR)
            server.close()
