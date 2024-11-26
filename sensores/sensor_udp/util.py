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
        return {
            "userid": self.id,
            "type": self.type,
            "value1": self.value1,
            "value2": self.value2,
            "inhouse": True,
        }


class Generator:
    def __init__(self):
        # Parametros de controle de suavização de geração de valores aleatórios
        self.smoothing_factors = {
            1: {"value1_smooth": 0.7, "value2_smooth": 0.7},  # Pressão Sanguínea
            2: {"value1_smooth": 0.8, "value2_smooth": 0.8},  # SPO2 e batimento cardíaco
            3: {"value1_smooth": 0.9},  # Temperatura corporal
        }

        # Estados gerados anteriormente - para geração aleatória mas com coerência
        self.previous_states: Dict[int, Dict[str, Any]] = {}

    def generate(self, active_users):
        for user in active_users:
            user_type_key = (user.id, user.type)
            prev_state = self.previous_states.get(
                user_type_key, {"value1": user.value1, "value2": user.value2}
            )
            # Determina se os valores gerados nessa passada serão anormais ou normais
            normal = random.randint(1, 10) <= 8

            if user.type == 1:  # Pressão Sanguínea
                if normal:
                    # Normal range
                    value1 = self._smooth_generate(
                        prev_state["value1"],
                        110,
                        129,
                        self.smoothing_factors[1]["value1_smooth"],
                    )
                    value2 = self._smooth_generate(
                        prev_state["value2"],
                        70,
                        84,
                        self.smoothing_factors[1]["value2_smooth"],
                    )
                else:
                    # Abnormal range (variação mais significativa)
                    value1 = self._smooth_generate(prev_state["value1"], 0, 300, 0.5)
                    value2 = self._smooth_generate(prev_state["value2"], 0, 300, 0.5)

                user.value1 = int(value1)
                user.value2 = int(value2)

            elif user.type == 2:  # SPO2 e batimento cardíaco
                if normal:
                    # SPO2 - normal range
                    value1 = self._smooth_generate(
                        prev_state["value1"],
                        95,
                        100,
                        self.smoothing_factors[2]["value1_smooth"],
                    )
                    # Batimentos - normal range
                    value2 = self._smooth_generate(
                        prev_state["value2"],
                        50,
                        100,
                        self.smoothing_factors[2]["value2_smooth"],
                    )
                else:
                    # Abnormal ranges
                    value1 = self._smooth_generate(prev_state["value1"], 0, 100, 0.5)
                    value2 = self._smooth_generate(prev_state["value2"], 0, 220, 0.5)

                user.value1 = int(value1)
                user.value2 = int(value2)

            elif user.type == 3:  # Temperatura corporal
                if normal:
                    # Normal range
                    value1 = self._smooth_generate(
                        prev_state["value1"],
                        36.0,
                        37.5,
                        self.smoothing_factors[3]["value1_smooth"],
                    )
                else:
                    # Abnormal range
                    value1 = self._smooth_generate(
                        prev_state["value1"], 30.0, 45.0, 0.5
                    )

                user.value1 = round(value1, 2)
                user.value2 = 0

            self.previous_states[user_type_key] = {
                "value1": user.value1,
                "value2": user.value2,
            }

        return active_users

    def _smooth_generate(self, prev_value, min_val, max_val, smooth_factor=0.7):
        """
        Gera um novo valor aleatório baseado no valor gerado anteriormente, para suavizar os dados finais

        :param prev_value: Valor anterior
        :param min_val: Valor mínimo possível
        :param max_val: Valor máximo possível
        :param smooth_factor: Controla quão próximo o novo valor está do valor anterior
        :return: Novo valor gerado
        """
        # Variação aleatória
        variation = random.uniform(-1, 1)

        # Cálculo do valor suavizado
        new_value = (
            smooth_factor * prev_value
            + (1 - smooth_factor) * (min_val + (max_val - min_val) * random.random())
            + variation
        )

        # Garantindo que o valor final estará dentro dos limites min/max
        return max(min_val, min(max_val, new_value))


class DataBase:
    def __init__(self):
        load_dotenv()

    def returnActiveUsers(self):
        url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(url)
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
                    cursor.execute(
                        """
                        SELECT value1, value2, datetime 
                        FROM collected_data 
                        WHERE userid = %s AND type = %s 
                        ORDER BY dateTime DESC 
                        LIMIT 1;
                    """,
                        (user_id, type_id),
                    )

                    recent_data = cursor.fetchone()

                    # Só adiciona o usuário se houverem dados
                    if recent_data:
                        value1, value2, dateTime = recent_data
                        user_obj = User(
                            id=user_id,
                            type=type_id,
                            value1=value1,
                            value2=value2,
                            dateTime=dateTime,
                        )
                        users.append(user_obj)
                    else:
                        user_obj = User(
                            id=user_id, type=type_id, value1=0, value2=0, dateTime=None
                        )
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
        data = {"username": admin_email, "password": admin_password}
        response = requests.post(self.auth_url, data=data)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            self.token = None

    def post_users(self, users):
        if self.token == None:
            return
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        for user in users:
            data = user.to_dict()
            response = requests.post(self.api_url, json=data, headers=headers)
            if response.status_code == 200:
                print("Usuário enviado com sucesso!")
            else:
                print(
                    f"Erro ao enviar usuário: {response.status_code} - {response.text}"
                )
