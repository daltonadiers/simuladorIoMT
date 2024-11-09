import random 

class User:
    def __init__(self, id, type, value1, value2, dateTime):
        self.id = id
        self.type = type
        self.value1 = value1
        self.value2 = value2
        self.dateTime = dateTime

    def to_dict(self):
        return {"id": self.id, "type": self.type, "value1":self.value1, "value2":self.value2}
    
class Generator:
    def generate(active_users):
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
