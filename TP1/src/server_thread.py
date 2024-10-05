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