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
        self.__user_profile_pic = "avatar.jpg"

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

# #This is where we access the cart
# class Cart():
#
#     count = 0
#
#     food_details = {'foodid1':["PRIME STEER RIBEYE", 28.90],
#             'foodid2':["IEAT SUPER BURGER", 28.90]
#             }
#
#     def __init__(self, food_id, food_quantity):
#         self.__food_id = food_id
#         self.__dict__food_details = Cart.food_details
#         self.__food_quantity = food_quantity
#         self.__food_count = Cart.count
#
# #Food accessor method
#     def get_food_id(self):
#         return self.__food_id
#
#     def get_food_quantity(self):
#         return self.__food_quantity
#
#     def get_food_details(self):
#         return self.__dict__food_details
#
#     def get_total_price(self):
#         return self.__dict__food_details[self.__food_id[1]] * self.__food_quantity
#
# #Set food method
#     def set_food_quantity(self, food_quantity):
#         self.__food_quantity = food_quantity

class Food():
    def __init__(self, name, description, price, picture):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__picture = picture

    def set_name(self, name):
        self.__name = name
    def set_description(self, description):
        self.__description = description
    def set_price(self, price):
        self.__price = price
    def set_picture(self, picture):
        self.__picture = picture

    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_price(self):
        return self.__price
    def get_picture(self):
        return self.__picture

    def __str__(self):
        return ' name:{} \n description:{} \n price:{} \n picture:{}'.format(self.get_name(), self.get_description(), self.__price, self.__picture)


# Setting and Retrieving Seating Plans
class Seat():
    count_id = 0

    def __init__(self, name, seat):
        Seat.count_id += 1
        self.__user_id = Seat.count_id
        self.__name = name
        self.__seat = seat

    def get_name(self):
        return self.__name

    def get_user_id(self):
        return self.__user_id

    def get_seat(self):
        return self.__seat

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_seat(self, seat):
        self.__seat = seat

# Setting and retrieving temperature


class TemperatureM():

    def __init__(self, temperaturemorning):
        self.__temperaturemorning = temperaturemorning

    def get_temperaturemorning(self):
        return self.__temperaturemorning

    def set_temperaturemorning(self,temperaturemorning):
         self.__user_temperaturemorning = temperaturemorning

    def _str_(self):
        return ' temperaturemorning: {} '.format(self.get_temperaturemorning())