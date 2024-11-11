import socket
import pickle
import json
import requests
from queue import Queue
from util import User

SERVERUDP = '127.0.0.1'
PORTUDP = 7777
api_url = "https://iomt-data-api-7752107602.us-central1.run.app/collected-data/"

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((SERVERUDP, PORTUDP))

def postToRest(user):
    data = user.to_dict()
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        print("Usuário enviado com sucesso!")
    else:
        print(f"Erro ao enviar usuário: {response.status_code} - {response.text}")

def main():    
    while True:
        data, endereco = udp_socket.recvfrom(2048)
        user = pickle.loads(data)
        postToRest(user)

if __name__ == "__main__":
    main()
