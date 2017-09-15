import socketserver
import sys
class MyUDPHandler(socketserver.BaseRequestHandler):
    # Словарь адресов пользователей (keys) и их имен (value), взаимодействующих с сервером
    # по этим адресам происходит рассылка сообщений чата
    client_base  = {}   
    message_size = 1024
    
    # Отправление сообщения ans, пользователям из client_base
    def mas_send(self, socket, ans):
        for client in self.client_base:
            socket.sendto(bytes(ans.encode('utf8')), client)
    
    # В зависимости от принимаемых данных различаются следующие типы сообщений:
    # ::new name - проверка есть ли имя name в client_base.values(), если имени нет, 
    #   оповещение о появлении нового пользователя name по всем адресам client_base.keys()
    # ::exit name - исключение name из client_base и отправка оповещения об этом всем адресам client_base.keys()
    # ::members - оправка информации о всех пользователях в сети client_base.values() запросившему пользователсю
    # name: "Text" - рассылка данного сообщения по всем адресам client_base
    # Если приходит запрос от пользователя, что имя не было инициализоровани в системе через
    # ::new - он отправляет сообщение ::exit. Такая ситуация возможна при перезапуске сервера
    def handle(self, ):
        data = self.request[0].decode(encoding='UTF-8').strip()
        socket = self.request[1]
        data = data[:self.message_size]
        print("{} wrote:".format(self.client_address))
        print(data)
        
        if not data.startswith("::"):
            name = data.strip()[:data.find(":")].split()
            name = " ".join(name)
            print(name)
            if name not in self.client_base.values():
                self.client_base[self.client_address] = name
                socket.sendto(bytes("::error_name".encode('utf8')), self.client_address)
                
        if data.startswith("::new"):
            name = data.strip().split()[1:]
            name = " ".join(name)
            print(name)
            if name in self.client_base.values() or name.find(":") != -1:
                socket.sendto(bytes("::no".encode('utf8')), self.client_address)
                return
            else:
                self.client_base[self.client_address] = name
                socket.sendto(bytes("::ok".encode('utf8')), self.client_address)
                ans = name + " присоеденился к чату!"
                print("В сети:")
                print(self.client_base)
                self.mas_send(socket, ans)
                return
                
        if data.startswith("::exit"):
            name = self.client_base[self.client_address]
            ans = name + " вышел и чата!"
            self.mas_send(socket, ans)
            self.client_base.pop(self.client_address, None)
            print("В сети:")
            print(self.client_base)
            return
        
        if data.startswith("::members"):
            ans = "В сети: \n"
            for name in self.client_base.values():
                ans += "\t" + name + "\n"
            socket.sendto(bytes(ans[:-1].encode('utf8')), self.client_address)
            return
       
        self.mas_send(socket, data)
        
        
# Считывание адреса и порта сервера из входных параметров, иначе 
# значения берутся по умолчанию.       
if __name__ == "__main__":
    
    try:
        print(sys.argv)
        if len(sys.argv) == 3:
            HOST, PORT = sys.argv[1], int(sys.argv[2])
        else:
            HOST, PORT = "localhost", 9090
        server = socketserver.UDPServer((HOST, PORT), MyUDPHandler) 
    except:
        print("Неверные аргументы, введите адрес и порт сервера")
        sys.exit(1)
    server.request_queue_size = 15
    print("Мой адрес: ", str((server.server_address)))
    print("Количество доступный подключений:", str(server.request_queue_size))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nЗакрытие сервера...")
    server.server_close()