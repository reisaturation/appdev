import shelve
import uuid
from passlib.hash import pbkdf2_sha256

class Admin():
    def __init__(self, username, user_pw):
        self.__username = username
        self.__user_pw = pbkdf2_sha256.hash(user_pw)
        self.__code = 's4fEc0dE'

    def get_username(self):
        return self.__username

    def get_user_pw(self):
        return self.__user_pw

    def get_code(self):
        return self.__code

    def __str__(self):
        return 'username: {} \n password:{} \n'.format(self.__username,self.get_user_pw())

class User():

    def __init__(self, user_email, username, user_pw, user_firstname, user_lastname):
        self.__user_id = uuid.uuid4().hex
        self.__user_email = user_email
        self.__username = username
        self.__user_pw = pbkdf2_sha256.hash(user_pw)
        self.__user_firstname = user_firstname
        self.__user_lastname = user_lastname
        self.__user_profile_pic = "avatar.jpg"
        self.__block_number = ''
        self.__postal_code = ''
        self.__review = ''
        self.__rating = ''

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

    def get_user_profile_pic(self):
        return self.__user_profile_pic

    def get_block_number(self):
        return self.__block_number

    def get_postal_code(self):
        return self.__postal_code

    def get_review(self):
        return self.__review

    def get_rating(self):
        return self.__rating

#User set methods

    def set_user_email(self,email):
        self.__user_email = email

    def set_username(self,username):
        self.__username = username

    def set_user_firstname(self,firstname):
        self.__user_firstname = firstname

    def set_user_lastname(self,lastname):
        self.__user_lastname = lastname

    def set_user_profile_pic(self,profile_pic):
        self.__user_profile_pic = profile_pic

    def set_block_number(self,block_number):
        self.__block_number = block_number

    def set_postal_code(self,postal_code):
        self.__postal_code = postal_code

    def set_review(self, review):
        self.__review = review

    def set_rating(self, rating):
        self.__rating = rating


    def __str__(self):
        return ' user_id:{} \n username: {} \n email: {} \n password:{} \n firstname:{} \n lastname:{} \n fullname:{}'.format(
            self.get_user_id(), self.get_username(), self.get_user_email(), self.get_user_pw(), self.get_user_firstname(), self.get_user_lastname(), self.get_user_fullname())


def get_user(userid):
    try:
        db = shelve.open('databases/user.db', 'r')
    except IOError:
        print("Error opening user.db")
    except:
        print("Unknown error occurred fetching user.db")
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
        print("Unknown error occurred fetching user.db")
    else:
        if user_obj.get_user_id() in db.keys():
            db[user_obj.get_user_id()] = user_obj
            db.close()


class Food():
    def __init__(self, name, description, price, picture, food_category):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__picture = picture
        self.__food_catgeory = food_category

    def set_name(self, name):
        self.__name = name
    def set_description(self, description):
        self.__description = description
    def set_price(self, price):
        self.__price = price
    def set_picture(self, picture):
        self.__picture = picture
    def set_food_category(self, food_category):
        self.__food_catgeory = food_category

    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_price(self):
        return self.__price
    def get_picture(self):
        return self.__picture
    def get_food_category(self):
        return self.__food_catgeory

    def __str__(self):
        return ' name:{} \n description:{} \n price:{} \n picture:{} \n category:{}'.format(self.get_name(), self.get_description(), self.__price, self.__picture, self.__food_catgeory)


# Setting and Retrieving Seating Plans
class Seat():
    count_id = 0

    def __init__(self, name, time, seat):
        Seat.count_id += 1
        self.__user_id = Seat.count_id
        self.__name = name
        self.__seat = seat
        self.__time = time

    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_time(self):
        return self.__time

    def get_seat(self):
        return self.__seat

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_time(self, time):
        self.__time = time

    def set_seat(self, seat):
        self.__seat = seat

# Setting and retrieving temperature


class TemperatureM():
    def __init__(self, temperaturemorning, temperatureafternoon, temperaturenight, username, declaration1, declaration2, declaration3, declaration4):
        self.__temperaturemorning = temperaturemorning
        self.__temperatureafternoon = temperatureafternoon
        self.__temperaturenight = temperaturenight
        self.__username = username
        self.__declaration1 = declaration1
        self.__declaration2 = declaration2
        self.__declaration3 = declaration3
        self.__declaration4 = declaration4


    def get_temperaturemorning(self):
        return self.__temperaturemorning

    def get_temperatureafternoon(self):
        return self.__temperatureafternoon

    def get_temperaturenight(self):
        return self.__temperaturenight

    def get_username(self):
        return self.__username

    def get_declaration1(self):
        return self.__declaration1

    def get_declaration2(self):
        return self.__declaration2

    def get_declaration3(self):
        return self.__declaration3

    def get_declaration4(self):
        return self.__declaration4



    def set_temperaturemorning(self,temperaturemorning):
         self.__user_temperaturemorning = temperaturemorning

    def set_temperatureafternoon(self,temperatureafternoon):
         self.__user_temperatureafternoon = temperatureafternoon

    def set_temperaturenight(self,temperaturenight):
         self.__user_temperaturenight = temperaturenight

    def set_username(self,username):
        self.__user_username = username

    def set_declaration1(self,declaration1):
        self.__user_declaration1 = declaration1

    def set_declaration2(self,declaration2):
        self.__user_declaration2 = declaration2

    def set_declaration3(self,declaration3):
        self.__user_declaration3 = declaration3

    def set_declaration4(self,declaration4):
        self.__user_declaration4 = declaration4



    def __str__(self):
        return ' temperaturemorning: {} \n temperatureafternoon: {} \n temperaturenight: {} \n username: {} \n declaration1:{} \n declaration2: {} \n declaration3: {} \n declaration4: {}'.format(self.get_temperaturemorning(), self.get_temperatureafternoon(), self.get_temperaturenight(), self.get_username(), self.get_declaration1(), self.get_declaration2(), self.get_declaration3(), self.get_declaration4())