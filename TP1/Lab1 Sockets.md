<html>
	<center>Distributed Architectures and Programming</center>
	<center>ISEP - October 2024</center>
	<center style="font-style:italic">by Quentin LAURENT and Theophile WEMAERE</center>
</html>

>[!NOTE]
>Codes for this lab can also be found on Github :
>https://github.com/Theophile-Wemaere/ArchProgDistr


# Part 1. Single Socket

For this first part, we will use a simple server listening for the first user to connect, and will process only the first user messages.

**Code for the server :**
```python
import socket
import sys

# global socket object 
s: socket.socket = None

def handle_client(conn, addr):
    # while true, wait for incoming user message, print them and send them back
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data from {str(addr)} :",data.decode('UTF-8'))
        conn.sendall(data)
    conn.close()

def main():

    global s

    HOST = "127.0.0.1"
    PORT = 8000

    # possibility of using non default args with command line
    print("\nUse ./server.py HOST PORT for non default args")
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

    # open socket with specified params
    # AF_INET : use HOST and PORT to declare socket
    # SOCK_STREAM : use TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            # when connection is received, send it to
            # the handle_client() function for msg processing
            conn, addr = s.accept()
            print('Connected by', addr)
            handle_client(conn, addr)

if __name__ == "__main__":
    try:
        main()
    # if user press Ctrl+C, exit by closing the socket
    except KeyboardInterrupt:
        print("Ctrl + C, exiting...")

if s != None:
    s.close()
```

**Code for the client :**
```python
import socket
import sys

# global socket object 
s: socket.socket = None

def main():

    global s

    HOST = "127.0.0.1"
    PORT = 8000
    # possibility of using non default args with command line
    print("\nUse ./client.py HOST PORT for non default args")
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

    # open socket with specified params
    # AF_INET : use HOST and PORT to declare socket
    # SOCK_STREAM : use TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}, use Ctrl+C to exit")
        while True:
            # wait for user input, encode msg and send it trought socket
            # then print data if reiceved
            msg = input("> ")
            s.sendall(str.encode(msg))
            data = s.recv(1024)
            if not data:
                continue
            else:
                print('Received  : ',data.decode('UTF-8'))

if __name__ == "__main__":
    try:
        main()
    # if user press Ctrl+C, exit by closing the socket
    except KeyboardInterrupt:
        print("Ctrl + C, exiting...")

if s != None:
    s.close()
```

Example of utilization with a simple communication client <-> server : 
![[img/img1.png]]
>[!TIP]
>You can use non default args by calling the scripts with command-line arguments
>For example to listen on `0.0.0.0` with port `1337`, you can use the following command :
>```shell
>$ python3 server.py "0.0.0.0" 1337

This kind of server work well with one client, but as the code only handle the first connection, any new client would not be able to connect and would not have his messages processed. We can remediate this by sending the `handle_client()` function in a separate thread, allowing the server to handle multiple clients at once.

# Part 2. MultiThreaded Client-Server communication using TCP sockets

For this part, we will use multi-threading so each client has his own thread to have his message processed.

**Code for the server :**
```python
import socket
import threading
import sys

# global socket object 
s: socket.socket = None
# global thread list
all_thread = []

def handle_client(conn, addr):
    # while true, wait for incoming user message, print them and send them back
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data from {str(addr)} :",data.decode('UTF-8'))
        conn.sendall(data)
    conn.close()

def main():

    global s, all_thread
    
    HOST = "127.0.0.1"
    PORT = 8000
    # possibility of using non default args with command line
    print("\nUse ./server_thread.py HOST PORT for non default args")
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

    # open socket with specified params
    # AF_INET : use HOST and PORT to declare socket
    # SOCK_STREAM : use TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            # instead of just calling the handle_client() function
            # declare and start a thread with the right arguments
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            thread.start()
            # also add thread object to global array
            # (to close them when terminating the program)
            all_thread.append(thread)

if __name__ == "__main__":

    try:
        main()
    # if user press Ctrl+C, exit by closing the socket
    except KeyboardInterrupt:
            print("Ctrl + C, exiting...")

if s != None:
    s.close()

# also join all the thread to terminate them
for thread in all_thread:
    thread.join()
```

As stated before, the main difference here is that instead of just calling the `handle_client()`, the server will launch a new thread which will handle the client messages.

When terminating the program, each thread will be joined to terminate them one by one.

Example of communication between multiples clients and single-thread server :
![[img/img2.png]]
We can see the server only accept one connection

Now with the multi_threaded server :
![[img/img3.png]]

# Part 3(Bonus). Multi-threaded group chat

For this part, we chose to implement a group chat in Python without a GUI.
The way it works is simple:
- The server waits for incoming connections from clients and create a separate thread for each client that connects
- Each client, when connected to the server, listens for incoming messages from the server (messages sent by other clients) and displays a prompt in the terminal allowing the user to send a message to the server

Whenever the server receives a message from one of the clients, it simply broadcasts the message to all clients (except the original sender, so that its message is not displayed twice on its terminal).

We have also implemented a graceful shutdown for both the client and the server:
- When a client shuts down, it sends an `EOF` to the server, which then closes the connection and terminates the thread dedicated to that client
- When the server shuts down, it closes all the connection (by sending an `EOF` to all clients) and terminates all the threads. The client process then exits gracefully upon receiving an `EOF` from the server.

Below is the code of the multithreaded server:

```python
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

```

Below is the code of the client:

```python
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

```

Example of use of the chat server and clients :
![[img/img4.png]]

We can see the broadcast system work as intended, and all users receive other users messages.