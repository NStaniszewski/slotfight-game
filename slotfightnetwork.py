import socket

class network():
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip=''
        self.port=5555
        self.address=(self.ip,self.port)
        self.pos=self.connect()
        #print(self.pos)

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except socket.error as err:
            print('net error: '+err)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as err:
            print('net error: '+err)

    def get_pos(self):
        return self.pos