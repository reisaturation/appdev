from Model import *
# import shelve
#
# db = shelve.open('databases/user.db')
# for user in db:
#     userObj = db[user]
#     print(userObj)
# db.close()

# db = shelve.open('databases/reviews.db')

# db = shelve.open('databases/food.db', 'w')
# food1 = Food('PRIME_STEER_RIBEYE', "ASTONS Prime Steer Ribeye is our customers' first choice. Not only value-for-money, but value for tummy! Tender - with a natural bite, in medium doneness it maintains a gentle trickle of moist natural steak juice. A wonderful dining experience - so satisfying thorough each cut portion.", 28.90, 'aston4.jpg')
# food2 = Food('IEAT_SUPER_BURGER','ASTONS massive ieat Super Burger is named after Singapore famous Blogger Dr Leslie. The big patty is grilled to perfection - Juicy and Moist! Combined with the crispy onion frost, streaky bacon, ASTONS special secret BBQ sauce, crunchy romaine lettuce, tomatoes, grilled bacon and cheddar cheese. This is easily the best tasting, value for money Burger in town.', 28.90, 'aston5.jpg')
# db['PRIME_STEER_RIBEYE'] = food1
# db['IEAT_SUPER_BURGER'] = food2
# db.close()
#
# db = shelve.open('databases/food.db')
# for food in db:
#     foodObj = db[food]
#     print(foodObj)
#     print()
#
# db.close()

# db = shelve.open('databases/temperature.db')
# for temp in db:
#     tempObj = db[temp]
#     print(tempObj)
#     print()

# db = shelve.open('databases/admin.db', 'w')
# admin1 = Admin('astonadmin','seCret4ston')
# db['main'] = admin1
# db.close()

db = shelve.open('databases/admin.db')
for admin in db:
    adminObj = db[admin]
    print(adminObj)
db.close()





