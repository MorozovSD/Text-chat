import socket
import os
from ctypes import *


GRAY = 8
BLUE = 9
GREEN = 10
TURQUOISE = 11
RED = 12
PINK = 13
YELLOW = 14
WHITE = 15

windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

def color_print(text, color):
    windll.Kernel32.SetConsoleTextAttribute(h, color)
    print(text.format( color ))
    windll.Kernel32.SetConsoleTextAttribute(h, WHITE)

os.system('cls' if os.name == 'nt' else 'clear')

sock = socket.socket()
sock.connect(('localhost', 9090))
while True:
    str = input("User: ")
    sock.send(bytes(str.encode('utf8')))
    data = sock.recv(1024)
    #to_pr = ":" + str(data.upper(),'utf-8')
    color_print(data.decode(encoding='UTF-8'), BLUE)
sock.close()

print(data)