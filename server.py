import os
import json 
from socket import socket, timeout, AF_INET, SOCK_STREAM
from threading import Thread
from time import time

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

        self.running = True
        self.buffer = bytes()

    def run(self):
        self.conn.settimeout(self.timeout)
        with self.conn:
            while self.running:
                try:
                    data = self.conn.recv(1024)
                except timeout:
                    ip, port = self.addr
                    print(f'Connection {ip}/{port} timed out.')
                    break 

                if not data:
                    continue

                self.handle_data(data)

        self.dump_buffer()
        self.conn.close()
    
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
        try:
            while True:
                conn, addr = sock.accept()
                client = ClientHandler(conn, addr)
                client.start()
                clients.append(client)
        except KeyboardInterrupt:
            print()
        
        for client in clients:
            client.running = False

        print('Waiting for clients to finish connection.')

        for client in clients:
            client.join()
        
        print('Disconecting Server.')


def read_config(path):
    config = dict()
    try:
        with open(path) as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f'Config file not found in {path}')
        print('Using default parameters.')
    return config

if __name__ == '__main__':
    config = read_config('config.json')
    start_server(**config)