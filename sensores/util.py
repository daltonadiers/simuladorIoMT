import random 
import psycopg2
import os
from dotenv import load_dotenv
import requests

class User:
    def __init__(self, id, type, value1, value2, dateTime):
        self.id = id
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.dateTime = dateTime

    def to_dict(self):
        return {"userid": self.id, "type": self.type, "value1":self.value1, "value2":self.value2, "inhouse":True}

class Generator:
    def generate(self, active_users):
        for i in active_users:
            if i.type == 1:
                i.value1 = random.randint(0, 300)
                i.value2 =  random.randint(0, 300)
            elif i.type == 2:
                i.value1 = random.randint(0, 100)
                i.value2 = random.randint(0, 200)
            elif i.type == 3:
                i.value1 = random.randint(30, 45)
                i.value2 = 0
        return active_users

class DataBase:
    def __init__(self):
        load_dotenv()

    def returnActiveUsers(self):
        url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(
            url
        )
        cursor = conn.cursor()
        users = []
        try:
            # Primeiro, busca todos os usuários ativos
            cursor.execute("SELECT seq FROM users WHERE active = TRUE;")
            active_users = cursor.fetchall()

            for user in active_users:
                user_id = user[0]

                # Busca todos os tipos associados ao usuário
                cursor.execute("SELECT type FROM types WHERE userid = %s;", (user_id,))
                user_types = cursor.fetchall()

                for user_type in user_types:
                    type_id = user_type[0]

                    # Busca o dado coletado mais recente para cada tipo e usuário
                    cursor.execute("""
                        SELECT value1, value2, datetime 
                        FROM collected_data 
                        WHERE userid = %s AND type = %s 
                        ORDER BY dateTime DESC 
                        LIMIT 1;
                    """, (user_id, type_id))
                    
                    recent_data = cursor.fetchone()

                    # Só adiciona o usuário se houverem dados
                    if recent_data:
                        value1, value2, dateTime = recent_data
                        user_obj = User(id=user_id, type=type_id, value1=value1, value2=value2, dateTime=dateTime)
                        users.append(user_obj)
                    else:
                        user_obj = User(id=user_id, type=type_id, value1=0, value2=0, dateTime=None)
                        users.append(user_obj)
        except Exception as e:
            print(f"Erro ao realizar consultas: {e}")
        finally:
            cursor.close()
            conn.close()
        return users
    
class postToRest:
    api_url = "https://iomt-data-api-7752107602.us-central1.run.app/collected-data/"
    auth_url = "https://iomt-data-api-7752107602.us-central1.run.app/token"
    def __init__(self):
        load_dotenv()
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        data={"username":admin_email, "password":admin_password}
        response = requests.post(self.auth_url, data=data)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            self.token = None
    
    def post_users(self, users):
        if(self.token == None):
            return
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        for user in users:
            data = user.to_dict()
            response = requests.post(self.api_url, json=data, headers=headers)
            if response.status_code == 200:
                print("Usuário enviado com sucesso!")
            else:
                print(f"Erro ao enviar usuário: {response.status_code} - {response.text}")