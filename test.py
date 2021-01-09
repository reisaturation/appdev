import shelve
db = shelve.open('databases/user.db')
for user in db:
    userObj = db[user]
    print(userObj)

