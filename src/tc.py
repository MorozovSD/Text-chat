import socket
from threading import Thread
import os
import sys


# История сообщений, с момента подключения к чату
history = []
# Количество отображаемых строк в чате берется со знаком "-", 
# т.к. это фактичски последние N элементов списка history
PRINT_SIZE = -50

# Флаг отвечающий за работу потоков приема и передачи сообщений
is_alive = True

# Считываем адрес и порт сервера из входных параметров, иначе берем
# значения по умолчанию.
# TODO добавить проверку корректности ввода
if len(sys.argv) == 3:
  HOST, PORT = sys.argv[1], sys.argv[2]
else:
    HOST, PORT = "localhost", 9090
sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )

# Вывод в консоль PRINT_SIZE строк из истории сообщений     
def print_hist():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*history[PRINT_SIZE:], sep='\n')

# Функция работы потока по приему сообщений от сервера.
# Принимается по 1024 символа
# TODO более красивый try-except блок 
# Поменять способ отображения сообщений на экран   
def recive_thread():
    global is_alive
    while is_alive:
        try:
            message = sock.recv(1024)
            history.append(message.decode(encoding='UTF-8'))
            print_hist()
        except:
            print("Ошибка!")
            is_alive = False

# Функция работы потока по отправки сообщений на сервер.
# nick - Идентификатор пользователя (оно же имя)
# Различается 3 типа сообщений:
# ::exit nick - выход из программы
# ::members - запрос на вывод всех членов чата
# nick: "Text" - отправка сообщения
# TODO более красивый try-except блок.
# Любой выход из программы должен посылать ::exit серверу
# Сделать более красивый ввод в формате "nick: text"  
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

# ::new nick - запрос на разрешение использования идентификатора nick
# recive_th - поток приема сообщений от сервера
# send_th - поток передачи сообщений на сервер
# TODO добавить обработку ошибок
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