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