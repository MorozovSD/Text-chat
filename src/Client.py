import socket
import os

os.system('cls' if os.name == 'nt' else 'clear')

sock = socket.socket()
sock.connect(('localhost', 9090))
while True:
    str = input()
    sock.send(bytes(str.encode('utf8')))
    data = sock.recv(1024)
    #to_pr = ":" + str(data.upper(),'utf-8')
    print(data.decode(encoding='UTF-8'))
sock.close()

print(data)