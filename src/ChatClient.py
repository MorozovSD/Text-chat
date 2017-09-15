import socket
from threading import Thread
import os
import sys

# История сообщений, с момента подключения к чату
history = []

# Количество отображаемых строк в чате берется со знаком "-", 
# т.к. это фактичски последние N элементов списка history
PRINT_SIZE = -50
MESSAGE_SIZE = 1024
NICK_SIZE = 16
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
except Exception as e:
    print("Неверные аргументы, введите адрес и порт сервера")
    print(e)
    
# Вывод в консоль PRINT_SIZE строк из истории сообщений     
def print_hist():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(*history[PRINT_SIZE:], sep='\n')

# при выходе из программу подается сообщение о выходе серверу
# История сообщений записывается в файл... Просто так
def exit():
    global is_alive
    message = "::exit " + nick
    sock.sendto(bytes(message.encode('utf8')), (HOST, PORT))
    is_alive = False
    with open("hist.txt", "w") as outf:
        for message in history:
            outf.write(message + "\n")
    print("Выход из программы...")
    
# Функция работы потока по приему сообщений от сервера.
# Принимается по MESSAGE_SIZE символа
# Поменять способ отображения сообщений на экран   
def receive_thread():
    global is_alive, nick
    while is_alive:
        try:
            message = sock.recv(MESSAGE_SIZE).decode(encoding='UTF-8')
            if message.startswith("::error_name"):
                print("Потеря данных на сервере, перезайдите")
                is_alive = False
                continue
            history.append(message)
            print_hist()
            print("$")
        except socket.timeout as e:
            continue
        except OSError as e:
            if e.errno == 10040:
                print("Error: Принимаемое сообщение оказалось слишком велико")
                continue
            elif e.errno == 10054:
                print("Сервер недоступен")
                exit()
            else:
                print(e)
                exit()
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
            command = input()
            if command == "":
                print_hist()
                continue
            elif command == ":exit":
                message = "::exit " + nick
                sock.sendto(bytes(message.encode('utf8')), (HOST, PORT))
                is_alive = False
            elif command == ":members":
                message = "::members"
                sock.sendto(bytes(message.encode('utf8')), (HOST, PORT))   
            else:
                message = nick + ": " + command
                sock.sendto(bytes(message.encode('utf8')), (HOST, PORT))
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
            print("Ваше имя должно содержать значимые символы, исключая \':\'")
            print("Размер длинна не должен превышать ", NICK_SIZE, "символов")
            nick = input("Введите имя:").strip()
            if (nick == ""):
                print("Некорректное имя. Попробойту нажать что-то кроме пробела и Tab'а")
                continue
            if (len(nick) > NICK_SIZE):
                print("Слишком длинное имя. Выберите более короткое имя.")
                continue
            message = "::new " + nick
            sock.sendto(bytes(message.encode('utf8')), (HOST, PORT))
            message = sock.recv(MESSAGE_SIZE).decode(encoding='UTF-8')
            if message.startswith("::ok"):
                break
            else:
                print("Ваше имя занято или имеет неправильный формат")
                print("Имя недолжно содержать \":\"")
        except socket.timeout as e:
            print("Сервер что-то молчит... Повторная попытка авторизации")
            continue
        except Exception as e:
            print(e)
            sys.exit(1)    
    return nick

# recive_th - поток приема сообщений от сервера
# send_th - поток передачи сообщений на сервер
if __name__ == "__main__":
    nick = ident()
    
    recive_th = Thread(target=receive_thread).start()
    send_th = Thread(target=send_thread, args = [nick]).start()