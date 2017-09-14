import socket
from threading import Thread
import os

history = []
members = {}
is_alive = 0

sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(('0.0.0.0',9110))

def check_mess(str):
    if str.startswith("::"):
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
        message = message.decode(encoding='UTF-8')
        if check_mess(message):
            history.append(message)
            print_hist()
        else:
            if message.startswith("::check"):
                str = message.split()
                if str[2] in members:
                    sock.sendto(bytes("::occupied".encode('utf8')), ('255.255.255.255',9110))
                else:
                    ans = ":: free" + members
                    members[ans] = ""
                    sock.sendto(bytes(ans.encode('utf8')), ('255.255.255.255',9110))
            
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
            sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',9110))
            is_alive = 0
        else:
            sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',9110))


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        nick = input("Введите имя:")
        str = "::check " + nick
        sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',9110))
        message = sock.recv(128)
        print(message)
        message = message.decode(encoding='UTF-8')
        print(message)
        if message.startwith("::free"):
            members = eval(message[6:])
            break
        else:
            print("Кажется имя уже занято. Используйте другое имя")
            continue
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(nick + ": ")
    str = "Пользователь " + nick + " присоеденился к чату"
    sock.sendto(bytes(str.encode('utf8')), ('255.255.255.255',9110))
    recive_th = Thread(target=recive).start()
    send_th = Thread(target=send, args = [nick]).start()

