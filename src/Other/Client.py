import socket
import os
from ctypes import windll, c_ulong

# TODO цветную печать в отдельный модуль
# Define color const
GRAY = 7
#BLUE = 9
#GREEN = 10
#TURQUOISE = 11
#RED = 12
#PINK = 13
#YELLOW = 14
WHITE = 15

# Some stuf for using color text in consol
windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))


servercol = WHITE

def color_print(text, color):
    windll.Kernel32.SetConsoleTextAttribute(h, color)
    print(text.format(color))
    windll.Kernel32.SetConsoleTextAttribute(h, GRAY)

    
os.system('cls' if os.name == 'nt' else 'clear')

sock = socket.socket()
sock.connect(('localhost', 9090))
nick = input("Select nickname:")
while True:
    str = input(nick + ":")
    sock.send(bytes(str.encode('utf8')))
    data = sock.recv(1024)
    if data.decode(encoding='UTF-8') == "--exit":
        break
    color_print(data.decode(encoding='UTF-8'), servercol)
sock.close()

#TODO отдельный поток для приема данных от сервера, когда перехожит в этот поток - он захватывает управление?
#https://habrahabr.ru/post/319706/
#