import socket
import threading
import sys

listener = None

def listen(s):

    while True:
        data = s.recv(1024)
        if not data:
            continue
        else:
            print('\n',data.decode('UTF-8')+"\nMessage : ")


def main():

    if len(sys.argv) < 4:
        print("use ./client.py HOST PORT PSEUDO")
        exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    PSEUDO = sys.argv[3]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        global listener
        listener = threading.Thread(target=listen, args=(s,))
        listener.start()
        while True:
            msg = input("Message : ")
            # remove useless thing
            msg = msg[msg.find('Message : ')+10:]
            s.sendall(str.encode(PSEUDO+":"+msg))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if listener != None:
            listener.join()
        exit(0)