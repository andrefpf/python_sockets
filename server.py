import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import time

from config import CONFIG


DEFAULT_PORT = 65432
DEFAULT_MAX_SIZE = 50
DEFAULT_TIMEOUT = 10
DEFAULT_FILENAME = 'PREFIX'
DEFAULT_PATH = 'database/'


class ClientHandler(Thread):
    def __init__(self, conn, addr, **kwargs):
        super().__init__()

        self.conn = conn
        self.addr = addr 

        self.max_size = kwargs.get('MAX_SIZE', DEFAULT_MAX_SIZE)
        self.filename = kwargs.get('FILENAME', DEFAULT_FILENAME)
        self.timeout  = kwargs.get('TIMEOUT',  DEFAULT_TIMEOUT)
        self.path     = kwargs.get('PATH',     DEFAULT_PATH)

        self.buffer = bytes()

    def run(self):
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                self.handle_data(data)
        self.dump_buffer()
    
    def handle_data(self, data):
        self.show_data(data)

        self.buffer += data
        while len(self.buffer) >= self.max_size:
            self.dump_buffer()
            self.buffer = self.buffer[self.max_size:]

    def show_data(self, data):
        ip, port = self.addr
        print(f'{ip}/{port}:    ', str(data, 'utf-8'))

    def dump_buffer(self):
        if len(self.buffer) == 0:
            return

        length = min(len(self.buffer), self.max_size)
        data = self.buffer[:length]

        ip, port = self.addr
        ip = ip.replace('.', '')

        timestamp = int(time())
        filename  = f'{self.path}/{self.filename}_{ip}_{port}_{timestamp}.txt'

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        with open(filename, 'wb') as file:
            file.write(data)


def start_server(**kwargs):
    port = kwargs.get('PORT', DEFAULT_PORT)

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(('', port))
        sock.listen()

        clients = []
        while True:
            conn, addr = sock.accept()
            client = ClientHandler(conn, addr)
            client.start()
            clients.append(client)
        
        for client in clients:
            client.join()


if __name__ == '__main__':
    start_server(**CONFIG)