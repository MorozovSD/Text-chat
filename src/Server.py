import socket

    
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)
ans_list = ["Привет " + addr[0], "мммм, как интересно", "продолжай))"]
i = 0
while True:
    data = conn.recv(1024)
    ans = "Your_friend:" + ans_list[i]
    conn.send(ans.encode('utf8'))
    i = (i+1) % len(ans_list)
conn.close()