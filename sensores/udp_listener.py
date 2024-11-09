import socket
import pickle
from queue import Queue
from util import User

SERVERUDP = '127.0.0.1'
PORTUDP = 7777

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SERVERUDP, PORTUDP))

def postToRest(user):
    pass

def main():    
    while True:
        data, endereco = udp_socket.recvfrom(2048)
        user = pickle.loads(data)
        postToRest(user)
        print(user.type)

if __name__ == "__main__":
    main()
