import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)
    ans = addr[0] + ":" + str(data.upper(),'utf-8')
    conn.send(ans.encode('utf8'))

conn.close()