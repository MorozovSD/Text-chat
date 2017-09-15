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
try:
    if len(sys.argv) == 3:
      HOST, PORT = sys.argv[1], sys.argv[2]
    else:
        HOST, PORT = "localhost", 9090
    sock = socket.socket()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
    sock.settimeout(1)
except:
    print("Ошибка ввода адреса сервера и/или порта")
    
# Вывод в консоль PRINT_SIZE строк из истории сообщений     
def print_hist():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*history[PRINT_SIZE:], sep='\n')

# при выходе из программу подается сообщение о выходе серверу
# История сообщений записывается в файл... Просто так
def exit():
    global is_alive
    mess = "::exit " + nick
    sock.sendto(bytes(mess.encode('utf8')), (HOST, PORT))
    is_alive = False
    with open("hist.txt", "w") as outf:
        for mess in history:
            outf.write(mess + "\n")
    print("Выход из программы...")
    
# Функция работы потока по приему сообщений от сервера.
# Принимается по 1024 символа
# Поменять способ отображения сообщений на экран   
def recive_thread():
    global is_alive, nick
    while is_alive:
        try:
            message = sock.recv(1024).decode(encoding='UTF-8')
            if message.startswith("::error_name"):
                print("Потеря данный на сервере, перезайдите")
                is_alive = False
                continue
            history.append(message)
            print_hist()
            print("$")
        except socket.timeout as e:
            continue
        except OSError as e:
            print("Error: Принимаемое сообщение оказалось слишком велико")
            continue
        except Exception as e:
            print(e)
            exit()

# Функция работы потока по отправки сообщений на сервер.
# nick - Идентификатор пользователя (оно же имя)
# Различается 3 типа сообщений:
# ::exit nick - выход из программы
# ::members - запрос на вывод всех членов чата
# nick: "Text" - отправка сообщения
# TODO обработка ctrl+c // в потоках нельзя
def send_thread(nick):
    global is_alive
    while is_alive:
        try:
            s = nick + ": " + input("$")
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
        except (EOFError, KeyboardInterrupt):
            exit()
        except Exception as e:
            print(e)
            continue
            
# Определение имени
# ::new nick - запрос на разрешение использования идентификатора nick
def ident():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            nick = input("Select nickname:")
            s = "::new " + nick
            sock.sendto(bytes(s.encode('utf8')), (HOST, PORT))
            message = sock.recv(1024).decode(encoding='UTF-8')
            if message.startswith("::ok"):
                break
        except socket.timeout as e:
            print("Сервер что-то молчит... Чтож попробуем еще разок")
            continue
        except Exception as e:
            print(e)
            sys.exit(1)    
    return nick

# recive_th - поток приема сообщений от сервера
# send_th - поток передачи сообщений на сервер
if __name__ == "__main__":
    nick = ident()
    
    recive_th = Thread(target=recive_thread).start()
    send_th = Thread(target=send_thread, args = [nick]).start()