import socket
import threading

clients = {}
t_all = []

def handle_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received data from  {addr}: {data}")
        data = data.decode('UTF-8')
        pseudo = data[:data.find(':')]
        data = data[data.find(':')+1:]
        for client in clients:
            if client != addr:
                print(client,addr)
                conn = clients[client]["conn"]
                data = f"{pseudo} > {data}"
                try:
                    print(data)
                    conn.sendall(str.encode(data))
                except ConnectionResetError:
                    clients[addr]["thread"].join()
                    clients.pop(addr)
    conn.close()

s = None
def main():

    global clients, s
    
    HOST = '0.0.0.0'
    PORT = 8081
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            clients[addr] = {}
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            clients[addr]["thread"] = thread
            clients[addr]["conn"] = conn
            t_all.append(thread)
            thread.start()

if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
            print("Ctrl + C, exiting...")

if s != None:
    s.close()
for thread in t_all:
    thread.join()
if s!= None:
    s.close()