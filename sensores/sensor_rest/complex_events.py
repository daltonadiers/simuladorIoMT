import logging
from enum import Enum, auto


class EventSeverity(Enum):
    BAIXA = auto()
    MEDIA = auto()
    ALTA = auto()
    CRITICA = auto()


class ComplexHealthEventDetector:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def detect_complex_events(self, users):
        """
        Método principal para detectar eventos de saúde complexos para múltiplos usuários
        """
        complex_events = []
        for user in users:
            event = self._analyze_user_health(user)
            if event:
                complex_events.append(event)
        return complex_events

    def _analyze_user_health(self, user):
        """
        Detecção abrangente de eventos de saúde para um único usuário
        """
        current_reading = {
            "user_id": user.id,
            "type": user.type,
            "value1": user.value1,
            "value2": user.value2,
            "timestamp": user.dateTime,
        }

        if user.type == 1:  # Pressão sanguinea
            return self._detect_bp_events(current_reading)
        elif user.type == 2:  # SPO2 e batimentos cardiacos
            return self._detect_spo2_events(current_reading)
        elif user.type == 3:  # Temperatura corporal
            return self._detect_temperature_events(current_reading)

        return None

    def _detect_bp_events(self, reading):
        """
        Detecta eventos complexos relacionados à pressão arterial
        """
        systolic, diastolic = reading["value1"], reading["value2"]

        # Crise Hipertensiva
        if systolic > 180 and diastolic > 120:
            return {
                "user_id": reading["user_id"],
                "event_type": "CRISE_HIPERTENSIVA",
                "severity": EventSeverity.CRITICA,
                "description": "Pressão arterial extremamente alta - Atenção médica imediata necessária",
                "diagnostic_hint": "Risco potencial de derrame ou ataque cardíaco",
            }

        # Hipotensão
        if systolic < 90 and diastolic < 60:
            return {
                "user_id": reading["user_id"],
                "event_type": "HIPOTENSAO",
                "severity": EventSeverity.ALTA,
                "description": "Pressão arterial perigosamente baixa",
                "diagnostic_hint": "Potencial choque ou insuficiência circulatória",
            }

        return None

    def _detect_spo2_events(self, reading):
        """
        Detecta eventos complexos relacionados a SPO2 e frequência cardíaca
        """
        spo2, heart_rate = reading["value1"], reading["value2"]

        # Hipoxemia Severa
        if spo2 < 90 and heart_rate > 100:
            return {
                "user_id": reading["user_id"],
                "event_type": "HIPOXEMIA_SEVERA",
                "severity": EventSeverity.CRITICA,
                "description": "Saturação de oxigênio baixa com frequência cardíaca elevada",
                "diagnostic_hint": "Potencial falha respiratória ou comprometimento cardíaco",
            }

        # Bradicardia
        if heart_rate < 50:
            return {
                "user_id": reading["user_id"],
                "event_type": "BRADICARDIA",
                "severity": EventSeverity.ALTA,
                "description": "Frequência cardíaca anormalmente baixa",
                "diagnostic_hint": "Potenciais problemas no sistema de condução cardíaca",
            }

        # Taquicardia
        if heart_rate > 120:
            return {
                "user_id": reading["user_id"],
                "event_type": "TAQUICARDIA",
                "severity": EventSeverity.ALTA,
                "description": "Frequência cardíaca anormalmente alta",
                "diagnostic_hint": "Possível estresse, ansiedade ou problema cardíaco",
            }

        return None

    def _detect_temperature_events(self, reading):
        """
        Detecta eventos complexos relacionados à temperatura
        """
        temperature = reading["value1"]

        # Hiperplexia - Febre Extremamente Alta
        if temperature > 41.5:
            return {
                "user_id": reading["user_id"],
                "event_type": "HIPERPIREXIA",
                "severity": EventSeverity.CRITICA,
                "description": "Temperatura corporal perigosamente alta",
                "diagnostic_hint": "Potencial infecção grave ou resposta inflamatória aguda",
            }

        # Febre Alta
        if temperature > 39.0:
            return {
                "user_id": reading["user_id"],
                "event_type": "FEBRE_ALTA",
                "severity": EventSeverity.ALTA,
                "description": "Temperatura corporal acima do normal",
                "diagnostic_hint": "Potencial infecção ou resposta inflamatória",
            }

        # Hipotermia
        if temperature < 35.0:
            return {
                "user_id": reading["user_id"],
                "event_type": "HIPOTERMIA",
                "severity": EventSeverity.CRITICA,
                "description": "Temperatura corporal criticamente baixa",
                "diagnostic_hint": "Potencial exposição a risco metabólico ou ambiental",
            }

        return None

    def log_complex_events(self, complex_events):
        """
        Registra eventos de saúde complexos detectados
        """
        for event in complex_events:
            if event:
                severity_level = event["severity"].name
                self.logger.critical(
                    f"EVENTO DE SAÚDE COMPLEXO - User {event['user_id']}:"
                )
                self.logger.critical(f"Tipo de Evento: {event['event_type']}")
                self.logger.critical(f"Severidade: {severity_level}")
                self.logger.critical(f"Descrição: {event['description']}")
                self.logger.critical(
                    f"Possível diagnóstico: {event['diagnostic_hint']}"
                )


# FOR TESTING PURPOSES
# from datetime import datetime
# class User:
#     def __init__(self, id, type, value1, value2, dateTime):
#         self.id = id
#         self.type = type
#         self.value1 = value1
#         self.value2 = value2
#         self.dateTime = dateTime
#
#
# detector = ComplexHealthEventDetector()
# users = [
#     User(1, 1, 190, 125, datetime.now()),  # Pressão alta (crise hipertensiva)
#     User(
#         2, 2, 85, 105, datetime.now()
#     ),  # Saturação de oxigênio baixa (hipoxemia severa)
#     User(
#         3, 3, 42.0, None, datetime.now()
#     ),  # Temperatura corporal muito alta (hiperpirexia)
#     User(4, 1, 80, 55, datetime.now()),  # Hipotensão
#     User(5, 2, 97, 45, datetime.now()),  # Bradicardia
# ]
#
# complex_events = detector.detect_complex_events(users)
# detector.log_complex_events(complex_events)
