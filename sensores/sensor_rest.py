import json
import requests
from util import Generator, User, DataBase

api_url = "https://iomt-data-api-7752107602.us-central1.run.app/collected-data/"

def postToRest(users):
    for user in users:
        data = user.to_dict()
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print("Usuário enviado com sucesso!")
        else:
            print(f"Erro ao enviar usuário: {response.status_code} - {response.text}")


def main():    
    db = DataBase()
    users = db.returnActiveUsers()
    if len(users) > 0:
        sg = Generator()
        new_generation = sg.generate(users)
        postToRest(new_generation)

if __name__ == "__main__":
    main()