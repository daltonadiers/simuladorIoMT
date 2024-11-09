import socket
import json
from queue import Queue

SERVERUDP = '127.0.0.1'
PORTUDP = 5002

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SERVERUDP, PORTUDP))

def postToRest(data):
    pass

def main():    
    while True:
        data, endereco = udp_socket.recvfrom(2048)
        postToRest(data)

if __name__ == "__main__":
    main()
