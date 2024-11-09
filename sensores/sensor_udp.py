import json
import socket
from sensor_generator import Generator
import psycopg2
from datetime import datetime
import time

class User:
    def __init__(self, id, type, value1, value2, dateTime):
        self.id = id
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.dateTime = dateTime

    def to_dict(self):
        return {"id": self.id, "type": self.type, "value1":self.value1, "value2":self.value2}
    
def realizeQuerys():
    conn = psycopg2.connect(
        dbname="iomt",
        user="user",
        password="rebonatto",
        host="localhost",
        port="3306"
    )
    cursor = conn.cursor()
    users = []
    try:
        # Primeiro, busca todos os usuários ativos
        cursor.execute("SELECT id FROM usuarios WHERE active = TRUE;")
        active_users = cursor.fetchall()

        for user in active_users:
            user_id = user[0]

            # Busca todos os tipos associados ao usuário
            cursor.execute("SELECT id FROM tipo WHERE user_id = %s;", (user_id,))
            user_types = cursor.fetchall()

            for user_type in user_types:
                type_id = user_type[0]

                # Busca o dado coletado mais recente para cada tipo e usuário
                cursor.execute("""
                    SELECT value1, value2, dateTime 
                    FROM dadoscoletados 
                    WHERE user_id = %s AND tipo_id = %s 
                    ORDER BY dateTime DESC 
                    LIMIT 1;
                """, (user_id, type_id))
                
                recent_data = cursor.fetchone()

                # Apenas adiciona o usuário se houver dados coletados
                if recent_data:
                    value1, value2, dateTime = recent_data
                    user_obj = User(id=user_id, type=type_id, value1=value1, value2=value2, dateTime=dateTime)
                    users.append(user_obj) 
    except Exception as e:
        print(f"Erro ao realizar consultas: {e}")
    finally:
        cursor.close()
        conn.close()
    return users

def send_udp():
    pass

def main():    
    #while True:
    #    users = realizeQuerys()
    #    if len(users) > 0:
    #        sg = sensor_generator()
    #        nova_geracao = sg.generate()
    #        send_udp(nova_geracao)
    #    time.sleep(10000)
    conn = psycopg2.connect(
        dbname="iomt",
        user="user",
        password="rebonatto",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    users = []
    cursor.execute("SELECT id, name FROM users WHERE active = TRUE;")
    active_users = cursor.fetchall()
    print(active_users)

if __name__ == "__main__":
    main()
    
