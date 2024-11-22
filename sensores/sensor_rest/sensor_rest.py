from util import Generator, DataBase, postToRest
import time

def main():    
    while True:
        db = DataBase()
        users = db.returnActiveUsers()
        if len(users) > 0:
            sg = Generator()
            new_generation = sg.generate(users)
            pr = postToRest()
            pr.post_users(new_generation)
        time.sleep(3600)

if __name__ == "__main__":
    main()