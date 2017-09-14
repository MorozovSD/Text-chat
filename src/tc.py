import socket
from threading import Thread
import os
import sys

PRINT_SIZE = -50
history = []

is_alive = True

if len(sys.argv) == 3:
  HOST, PORT = sys.argv[1], sys.argv[2]
else:
    HOST, PORT = "localhost", 9090
sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )

        
def print_hist():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*history[PRINT_SIZE:], sep='\n')
    
def recive_thread():
    global is_alive
    while is_alive:
        try:
            message = sock.recv(256)
            history.append(message.decode(encoding='UTF-8'))
            print_hist()
        except:
            print("Ошибка!")
            is_alive = False
            
def send_thread(nick):
    global is_alive
    while is_alive:
        try:
            s = nick + ": " + input()
            if s == nick + ": ":
                print_hist()
                continue
            elif s.startswith(nick + ": :exit"):
                mess = "::exit " + nick
                sock.sendto(bytes(mess.encode('utf8')), (HOST, PORT))
                is_alive = False
            elif s.startswith(nick + ": :members"):
                mess = "::members"
                sock.sendto(bytes(mess.encode('utf8')), (HOST, PORT))
            else:
                sock.sendto(bytes(s.encode('utf8')), (HOST, PORT))
        except:
            continue


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        nick = input("Select nickname:")
        os.system('cls' if os.name == 'nt' else 'clear')
        s = "::new " + nick
        sock.sendto(bytes(s.encode('utf8')), (HOST, PORT))
        message = sock.recv(128).decode(encoding='UTF-8')
        if message.startswith("::ok"):
            break
    
    recive_th = Thread(target=recive_thread).start()
    send_th = Thread(target=send_thread, args = [nick]).start()