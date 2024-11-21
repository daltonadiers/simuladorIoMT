import socket
import pickle
from datetime import datetime
from util import Generator, DataBase

UDP_IP = "127.0.0.1"
UDP_PORT = 7777 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_udp(new_generation):
    for i in new_generation:
        data = pickle.dumps(i)
        sock.sendto(data, (UDP_IP, UDP_PORT))

def main():    
    db = DataBase()
    users = db.returnActiveUsers()
    if len(users) > 0:
        sg = Generator()
        new_generation = sg.generate(users)
        send_udp(new_generation)

if __name__ == "__main__":
    main()
    
