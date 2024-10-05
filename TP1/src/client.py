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