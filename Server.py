import socket

sock = socket.socket()

sock.bind(('', 9110))
sock.listen(1)
print("Слушаю 9110 порт...")
conn, addr = sock.accept()

while True:
    data = conn.recv(1024)
    conn.send(data.upper())
    if data == "EXIT":
        break
print("Закрываю соединение")
conn.close()