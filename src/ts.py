import socketserver
import sys

class MyUDPHandler(socketserver.BaseRequestHandler):
    client_base  = {}    
    client_names = {}
    
    def mas_send(self, socket, s):
        for client in self.client_base:
            socket.sendto(bytes(s.encode('utf8')), client)
            
    def handle(self):
        data = self.request[0].decode(encoding='UTF-8').strip()
        socket = self.request[1]
        
        print("{} wrote:".format(self.client_address))
        print(data)
        
        if data.startswith("::new"):
            name = data.split()[1]
            if name in self.client_names.keys():
                socket.sendto(bytes("::no".encode('utf8')), self.client_address)
                return
            else:
                self.client_names[name] = name
                socket.sendto(bytes("::ok".encode('utf8')), self.client_address)
                self.client_base[self.client_address] = ""
                s = name + " присоеденился к чату!"
                self.mas_send(socket, s)
                return
           
        if data.startswith("::exit"):
            name = data.split()[1]
            print(self.client_names)
            print(self.client_base)
            s = name + " вышел и чата!"
            self.mas_send(socket, s)
            self.client_names.pop(name, None)
            self.client_base.pop(self.client_address)
            return
        
        if data.startswith("::members"):
            s = "В сети: \n"
            for name in self.client_names.keys():
                s += name + "\n"
            print(s)
            socket.sendto(bytes(s[:-1].encode('utf8')), self.client_address)
            return
            
        self.mas_send(socket, data)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        HOST, PORT = sys.argv[1], sys.argv[2]
    else:
        HOST, PORT = "localhost", 9090
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        print("Мой адрес: ", str((server.server_address)))
        server.serve_forever()