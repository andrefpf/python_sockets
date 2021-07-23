from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from random import randint

MAX_SIZE = 10
PREFIX = 'FILE'
PORT = 2021


class ClientHandler(Thread):
    def __init__(self, conn, addr):
        super().__init__()

        self.conn = conn
        self.addr = addr 
        self.n = 0

        self.path = 'database/'
        self.buffer = bytes()

    def run(self):
        with conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                self.handle_data(data)
        self.dump_buffer()
    
    def handle_data(self, data):
        # self.show_data(data)

        self.buffer += data
        while len(self.buffer) >= MAX_SIZE:
            self.dump_buffer()
            self.buffer = self.buffer[MAX_SIZE:]

    def show_data(self, data):
        ip, port = self.addr
        print(f'{ip}/{port}:    ', str(data, 'utf-8'))

    def dump_buffer(self):
        length = min(len(self.buffer), MAX_SIZE)
        data = self.buffer[:length]

        timestamp = '10101'
        filename = PREFIX + timestamp + '.txt'

        with open(self.path + str(self.n), 'wb') as file:
            file.write(data)
        self.n += 1





with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()

    clients = []
    for i in range(1):
        conn, addr = s.accept()
        client = ClientHandler(conn, addr)
        client.start()
        clients.append(client)
    
    for client in clients:
        client.join()