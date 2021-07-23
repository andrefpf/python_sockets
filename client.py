import json
from socket import socket, AF_INET, SOCK_STREAM

def read_config(path):
    config = dict()
    try:
        with open(path) as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f'Config file not found in {path}')
        print('Using default parameters.')
    return config

config = read_config('config.json')

HOST = '127.0.0.1'
PORT = config.get('PORT', 65432)

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        message = input()
        if not message:
            break
        s.sendall(bytes(message, 'utf-8'))