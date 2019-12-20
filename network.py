import socket
import pickle
# Pickle decerialises objects into bytes and sends them
# Over a network, so it transforms an object into bytes and sends it
# Using pickle.dumps(), and the opposite using pickle.loads()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" # Change this
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() # Send a number 0 or 1
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data)) # Send a string and recieves an object
            return pickle.loads(self.client.recv(2048))# Object recieval
        except socket.error as e:
            print(e)
