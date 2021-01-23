import socket
import pickle

class Network:


    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.1.22'
        self.port = 5555
        self.addr = (self.server, self.port)
    
    def connect(self):
        try:
            self.clientsocket.connect(self.addr)
            print('post connect')
            return pickle.loads(self.clientsocket.recv(2048))
            print('post received data from server')
        except socket.error as e:
            print('Error Connecting/Receiving Data for Initial Connect\n', e)

    def send(self, data):
        try: 
            self.clientsocket.sendall(pickle.dumps(data))
            return pickle.loads(self.clientsocket.recv(2048))
        except socket.error as e:
            print(str(e))