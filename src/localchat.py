import socket
from threading import Thread
import os

history = []

is_alive = 1

sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('0.0.0.0',11719))

def check_mess(str):
    name = str[:str.find(":")]
    text = str[str.find(":"):]
    if text == ":":
        return False
    else:
        return True
        
def print_hist():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*history, sep='\n')
    print(nick + ':')
    
def recive():
    global is_alive
    while is_alive:
        message = sock.recv(128)
        if check_mess(message.decode(encoding='UTF-8')):
            history.append(message.decode(encoding='UTF-8'))
            print_hist()
            
def send(nick):
    global is_alive
    while is_alive:
        str = nick + ": " + input()
        if str == nick + ": ":
            print_hist()
            continue
        elif str.startswith(nick + ": exit"):
            print("Вы вышли из чата")
            str = "Пользователь " + nick + " покинул чат."
            sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',11719))
            is_alive = 0
        else:
            sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',11719))


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    nick = input("Select nickname:")
    os.system('cls' if os.name == 'nt' else 'clear')

    print(nick + ": ")
    str = "Пользователь " + nick + " присоеденился к чату"
    sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',11719))
    recive_th = Thread(target=recive).start()
    send_th = Thread(target=send, args = [nick]).start()

