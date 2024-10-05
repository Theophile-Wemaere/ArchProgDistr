# Server
import socket
def handle_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data)
        conn.sendall(data)
    conn.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        try:
            while True:
                conn, addr = s.accept()
                print('Connected by', addr)
                handle_client(conn, addr)
        except KeyboardInterrupt:
            s.close()
            exit(0)