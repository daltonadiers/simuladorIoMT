import random 
import psycopg2

class User:
    def __init__(self, id, type, value1, value2, dateTime):
        self.id = id
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.dateTime = dateTime

    def to_dict(self):
        return {"userid": self.id, "type": self.type, "value1":self.value1, "value2":self.value2}

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
    def returnActiveUsers(self):
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