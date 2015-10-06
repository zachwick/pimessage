import socket, threading
import sys

HOST = sys.argv[1] #'127.0.0.1'
PORT = int(sys.argv[2]) #51234 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()


class chatServer(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket  = socket
        self.address = address
        self.name    = ""
        
    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print '%s:%s connected.' % self.address
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            
            if 'name:' in data:
                for c in clients:
                    if self.address == c.address:
                        c.name = data[5:].rstrip()
                        print(c.name)
            for c in clients:
                (c_ipaddr, c_port) = self.address
                if c.name == "":
                    c.socket.send("<" + str(c_ipaddr) + ">: " + data)
                else:
                    c.socket.send("<" + c.name + ">: " + data)
        self.socket.close()
        print '%s:%s disconnected.' % self.address
        lock.acquire()
        clients.remove(self)
        lock.release()

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    print("Chat Server started at "+HOST+" on port "+str(PORT))
    print("Connect with `telnet "+HOST+" "+str(PORT)+"` in a terminal")
    chatServer(s.accept()).start()
