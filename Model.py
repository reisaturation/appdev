import shelve
import uuid
from passlib.hash import pbkdf2_sha256

class User():
    def __init__(self, user_email, username, user_pw, user_firstname, user_lastname):
        self.__user_id = uuid.uuid4().hex
        self.__user_email = user_email
        self.__username = username
        self.__user_pw = pbkdf2_sha256.hash(user_pw)
        self.__user_firstname = user_firstname
        self.__user_lastname = user_lastname

#User_Model Accessor
    def get_user_email(self):
        return self.__user_email

    def get_username(self):
        return self.__username

    def get_user_pw(self):
        return self.__user_pw

    def get_user_firstname(self):
        return self.__user_firstname

    def get_user_lastname(self):
        return self.__user_lastname

    def get_user_fullname(self):
        return self.__user_firstname + " " + self.__user_lastname

    def get_user_id(self):
        return self.__user_id

    def __str__(self):
        return ' user_id:{} \n username: {} \n email: {} \n password:{} \n firstname:{} \n lastname:{} \n fullname:{}'.format(
            self.get_user_id(), self.get_username(), self.get_user_email(), self.get_user_pw(), self.get_user_firstname(), self.get_user_lastname(), self.get_user_fullname())

def get_user(userid):
    try:
        db = shelve.open('databases/user.db', 'r')
    except IOError:
        print("Error opening user.db")
    except:
        print("Unknown error occured fetching user.db")
    else:
        if userid in db.keys():
            user = db.get(userid)
            db.close()
            return user
        else:
            print("Userid not found in user.db")

def update_user(user_obj):
    try:
        db = shelve.open('databases/user.db', 'r')
    except IOError:
        print("Error opening user.db")
    except:
        print("Unknown error occured fetching user.db")
    else:
        if user_obj.get_user_id() in db.keys():
            db[user_obj.get_user_id()] = user_obj
            db.close()