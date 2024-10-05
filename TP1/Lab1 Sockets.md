<html>
	<center>Distributed Architectures and Programming</center>
	<center>ISEP - October 2024</center>
	<center style="font-style:italic">by Quentin LAURENT and Theophile WEMAERE</center>
</html>


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

