import random 
from util import User

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
