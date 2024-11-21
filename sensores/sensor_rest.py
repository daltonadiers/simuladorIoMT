from util import Generator, DataBase, postToRest

def main():    
    db = DataBase()
    users = db.returnActiveUsers()
    if len(users) > 0:
        sg = Generator()
        new_generation = sg.generate(users)
        pr = postToRest()
        pr.post_users(new_generation)

if __name__ == "__main__":
    main()