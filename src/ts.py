import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    client_base  = {}
    name_base = {}

    def is_new(self, socket, client_address, name):
        if client_address not in self.client_base.keys():
            if name not in self.name_base.keys():
                return True
            else:
                str = "Error: имя" + name + "занято!"
                socket.sendto(bytes(str.encode('utf8')), client)
                return False
        else:
            return False
            
    def welcome(self, socket, client, name):
        str = "Добро пожаловать в чат, " + name
        socket.sendto(bytes(str.encode('utf8')), client)
        for cl in self.client_base:
            str = name + "присоеденился к чату"
            socket.sendto(bytes(str.encode('utf8')), cl)
        self.client_base[client] = name
        self.name_base[name] = ""
    
    def handle(self):
        data = self.request[0].decode(encoding='UTF-8').strip()
        socket = self.request[1]
        name = data[:data.find(":")]
        if self.is_new(socket, self.client_address, name):
            self.welcome(socket, self.client_address, name)
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        for client in self.client_base:
            socket.sendto(bytes(data.encode('utf8')), client)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9090
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.socket
        server.serve_forever()