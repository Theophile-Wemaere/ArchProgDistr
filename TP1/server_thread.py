# Server
import socket
import threading

def handle_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data)
        conn.sendall(data)
    conn.close()


t_all = []
s = None
def main():
    
    HOST = '127.0.0.1'
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            thread.start()
            t_all.append(thread)

if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
            print("Ctrl + C, exiting...")
            if s != None:
                s.close()

if s != None:
    s.close()
for thread in t_all:
    thread.join()