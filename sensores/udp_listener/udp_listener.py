import socket
import pickle
from util import postToRest

SERVERUDP = '127.0.0.1'
PORTUDP = 7777

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SERVERUDP, PORTUDP))

def main():    
    while True:
        data, endereco = udp_socket.recvfrom(2048)
        user = pickle.loads(data)
        users = [user]
        pr = postToRest()
        pr.post_users(list(users))

if __name__ == "__main__":
    main()
