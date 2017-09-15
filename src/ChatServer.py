import socketserver
import sys
class MyUDPHandler(socketserver.BaseRequestHandler):
    # Словарь адресов пользователей (keys) и их имен (value), взаимодействующих с сервером
    # по этим адресам происходит рассылка сообщений чата
    client_base  = {}   
    
    
    # Отправление сообщения s, пользователям из client_base
    def mas_send(self, socket, s):
        for client in self.client_base:
            socket.sendto(bytes(s.encode('utf8')), client)
    
    # В зависимости от принимаемых данных различаются следующие типы сообщений:
    # ::new name - проверка есть ли имя name в client_base.values(), если имени нет, 
    #   оповещение о появлении нового пользователя name по всем адресам client_base.keys()
    # ::exit name - исключение name из client_base и отправка оповещения об этом всем адресам client_base.keys()
    # ::members - оправка информации о всех пользователях в сети client_base.values() запросившему пользователсю
    # name: "Text" - рассылка данного сообщения по всем адресам client_base
    # Если приходит запрос от пользователя, что имя не было инициализоровани в системе через
    # ::new - он отправляет сообщение ::exit. Такая ситуация возможна при перезапуске сервера
    def handle(self):
        data = self.request[0].decode(encoding='UTF-8').strip()
        socket = self.request[1]
        
        print("{} wrote:".format(self.client_address))
        print(data)
        
        if not data.startswith("::"):
            name = data.split()[0][:-1]
            if name not in self.client_base.values():
                self.client_base[self.client_address] = name
                socket.sendto(bytes("::error_name".encode('utf8')), self.client_address)
                
        if data.startswith("::new"):
            name = data.split()[1]
            if name in self.client_base.values() or name.startswith("::"):
                socket.sendto(bytes("::no".encode('utf8')), self.client_address)
                return
            else:
                self.client_base[self.client_address] = name
                socket.sendto(bytes("::ok".encode('utf8')), self.client_address)
                s = name + " присоеденился к чату!"
                print("В сети:")
                print(self.client_base)
                self.mas_send(socket, s)
                return
                
        if data.startswith("::exit"):
            name = self.client_base[self.client_address]
            s = name + " вышел и чата!"
            self.mas_send(socket, s)
            self.client_base.pop(self.client_address, None)
            print("В сети:")
            print(self.client_base)
            return
        
        if data.startswith("::members"):
            s = "В сети: \n"
            for name in self.client_base.values():
                s += "\t" + name + "\n"
            socket.sendto(bytes(s[:-1].encode('utf8')), self.client_address)
            return
        
        self.mas_send(socket, data)
          
        
# Считывание адреса и порта сервера из входных параметров, иначе 
# значения берутся по умолчанию.       
if __name__ == "__main__":

    if len(sys.argv) == 3:
        HOST, PORT = sys.argv[1], sys.argv[2]
    else:
        HOST, PORT = "localhost", 9090
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.request_queue_size = 15
        print("Мой адрес: ", str((server.server_address)))
        print("Количество доступный подключений:", str(server.request_queue_size))
        server.serve_forever()