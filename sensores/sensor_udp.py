import socket
import pickle
import psycopg2
from datetime import datetime
import time
from util import User, Generator

UDP_IP = "127.0.0.1"
UDP_PORT = 7777 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def realizeQuerys():
    conn = psycopg2.connect(
        dbname="iomt",
        user="user",
        password="rebonatto",
        host="localhost",
        port="3307"
    )
    cursor = conn.cursor()
    users = []
    try:
        # Primeiro, busca todos os usuários ativos
        cursor.execute("SELECT id FROM users WHERE active = TRUE;")
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

def send_udp(new_generation):
    for i in new_generation:
        data = pickle.dumps(i)
        sock.sendto(data, (UDP_IP, UDP_PORT))

def main():    
    #while True:
        users = realizeQuerys()
        if len(users) > 0:
            sg = Generator()
            new_generation = sg.generate(users)
            send_udp(new_generation)

if __name__ == "__main__":
    main()
    
