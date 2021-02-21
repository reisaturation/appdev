from flask import Flask, render_template, request, redirect, url_for, session, flash
from Forms import *
from Model import *
from passlib.hash import pbkdf2_sha256
import shelve
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "verysecretkey"


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit('.')[1]
    if ext.upper() in app.config["ALLOWED_PROFILE_PIC_TYPE"]:
        return True
    else:
        return False

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/aston", methods=["POST", "GET"])
def aston():
    from datetime import date
    db = shelve.open('databases/reviews.db')
    # if db is empty
    if len(db) == 0:
        db['review'] = {}
    reviewlist = db['review']
    reviewform = Reviews(request.form)
    if session.get('loggedin'):
        user_id = session['user_id']
        if request.method == "POST" and reviewform.validate():
            name = session['username']
            profile_pic = session['profile_pic']
            review = request.form['review']
            today = date.today()
            date = today.strftime("%d-%b-%Y")
            if len(review) == 1 and review[0] == ' ':
                error = 'Please enter a meaningful review'
                return render_template("aston.html", form= reviewform, reviewlist= reviewlist, error= error)
            else:
                reviewdict = db['review']
                reviewdict[user_id] = [name, profile_pic, review, date]
                db['review'] = reviewdict

                if user_id in reviewlist:
                    flash('You have successfully editted your review')
                else:
                    flash('You have successfully added a review')
                db.close()

                return redirect(url_for('aston', form= reviewform, reviewlist= reviewlist))

        return render_template("aston.html", form= reviewform, reviewlist= reviewlist)
    else:
        return render_template("aston.html", form= reviewform, reviewlist= reviewlist)

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if session.get('adminlogin') == True:
        return redirect(url_for('adminhome'))
    else:
        adminform = AdminForm(request.form)
        if request.method == "POST" and adminform.validate():
            db = shelve.open('databases/admin.db', 'r')
            username = request.form['username'].lower()
            password = request.form['password']
            secretcode = request.form['code']
            for admin in db:
                admin = db[admin]
                if admin.get_username() == username and pbkdf2_sha256.verify(password, admin.get_user_pw()) == True and secretcode == admin.get_code():
                    session['adminlogin'] = True
                    session['food_pic'] = 'aston1.jpg'
                    db.close()
                    return redirect(url_for('adminhome'))

    return render_template("admin/login.html", form=adminform)

@app.route('/admin/logout')
def admin_logout():
    if session.get('adminlogin') == True:
        session.clear()
        # session['adminlogin'] = False
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route("/admin/home")
def adminhome():
    if session.get('adminlogin') == True:
        return render_template('admin/home.html')
    else:
        return redirect(url_for('admin_login'))

app.config["FOOD_PIC_UPLOADS"] = "static/images/aston" #initializiing path for future references
app.config["ALLOWED_PROFILE_PIC_TYPE"] = ["PNG","JPG","JPEG","GIF"]

@app.route("/admin/addfood", methods=["POST","GET"])
def createfood():
    food_form = FoodForm(request.form)
    if session.get('adminlogin') == True:
        if request.method == "POST" and food_form.validate():
            food_name = request.form['food_name']
            food_price = float(request.form['food_price'])
            food_description = request.form['food_description']
            food_category = request.form['food_category']
            db = shelve.open('databases/food.db', 'w')
            food_id = food_name
            for character in food_id:
                if character == " ":
                    food_id = food_id.replace(" ","_").upper()
                else:
                    food_id= food_id.upper()

            if request.files['image'].filename != "":
                image = request.files["image"]
                # our name attribute inside our input form field.  this will return a file object in this case should be image/png
                if not allowed_image(image.filename):
                    extensionerror = "That image extension is not allowed"
                    print(extensionerror)
                    return render_template('/profile/editprofile.html', form=form, extensionerror=extensionerror)
                else:
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["FOOD_PIC_UPLOADS"], filename))
                    food_pic = filename
                    session['food_pic'] = food_pic

                food = Food(food_name, food_description, food_price, food_pic, food_category)
                db[food_id] = food
                db.close()
                return redirect(url_for('viewfood'))
        return render_template("admin/addfood.html", form= food_form)
    else:
        return  redirect(url_for('admin_login'))

@app.route('/admin/viewfood', methods=["POST","GET"])
def viewfood():
    if session.get('adminlogin'):
        db = shelve.open('databases/food.db', 'r')
        food_list = {}
        signature_list = {}
        burger_list = {}
        chicken_list = {}
        side_list = {}
        for item in db:
            category = db[item].get_food_category()
            food_list[db[item].get_name()] = [db[item].get_food_category()]
            if category == "signature":
                signature_list[db[item].get_name()] = [db[item].get_name(), db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
            elif category == "burger":
                burger_list[db[item].get_name()] = [db[item].get_name(), db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
            elif category == "chicken":
                chicken_list[db[item].get_name()] = [db[item].get_name(), db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
            elif category == "side":
                side_list[db[item].get_name()] = [db[item].get_name(), db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
        db.close()

        if request.method == "POST":
            if request.form['foodid']:
                food_id = request.form['foodid']
                food_id = food_id.replace(' ','_').upper()
                session['foodid'] = food_id
                return redirect(url_for('editfood'))
            elif request.form['deleteid']:
                food_id = request.form['deleteid']
                food_id = food_id.replace(' ', '_').upper()
                session['foodid'] = food_id
                return redirect(url_for('deletefood'))

        return render_template("admin/viewfood.html", foodlist=food_list, signaturelist=signature_list, burgerlist=burger_list, chickenlist=chicken_list, sidelist=side_list)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/editfood', methods=["GET","POST"])
def editfood():
    foodform = FoodForm(request.form)
    if session.get('adminlogin'):
        if not session.get('foodid'):
            return redirect(url_for('viewfood'))
        else:
            foodid = session['foodid'].upper()
            db = shelve.open('databases/food.db','r')
            fooditem = [db[foodid].get_name(), db[foodid].get_description(), db[foodid].get_price(), db[foodid].get_picture(), db[foodid].get_food_category()]
            db.close()

            if request.method == "POST" and foodform.validate():
                food_name = request.form['food_name']
                food_price = float(request.form['food_price'])
                food_description = request.form['food_description']
                food_category = request.form['food_category']
                if request.files['image'].filename != "":
                    image = request.files["image"]
                    # our name attribute inside our input form field.  this will return a file object in this case should be image/png
                    if not allowed_image(image.filename):
                        extensionerror = "That image extension is not allowed"
                        print(extensionerror)
                        return render_template('/profile/editprofile.html', form=form, extensionerror=extensionerror)
                    else:
                        filename = secure_filename(image.filename)
                        image.save(os.path.join(app.config["FOOD_PIC_UPLOADS"], filename))
                        food_pic = filename
                        session['food_pic'] = food_pic
                    db = shelve.open('databases/food.db', 'w')
                    food = db[foodid]
                    print(food)
                    if food.get_name() != food_name:
                        tempdb = db
                        tempdb.pop(foodid)
                        db = tempdb
                        foodid = food_name
                        for character in foodid:
                            if character == " ":
                                foodid = foodid.replace(" ", "_").upper()
                            else:
                                foodid = foodid.upper()

                        food = Food(food_name, food_description, food_price, food_pic, food_category)
                        db[foodid] = food
                        db.close()
                    else:
                        food.set_name(food_name)
                        food.set_price(food_price)
                        food.set_food_category(food_category)
                        food.set_description(food_description)
                        food.set_picture(food_pic)
                        db[foodid] = food
                    db.close()
                    return redirect(url_for('viewfood'))

        return render_template('admin/editfood.html', foodlist=fooditem, form=foodform)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/viewfood/<id>', methods=["POST","GET"])
def delete_food(id):
    foodid = id
    foodid = foodid.replace(' ','_').upper()
    db = shelve.open('databases/food.db','w')
    tempdb = db
    tempdb.pop(foodid)
    db = tempdb
    db.close()
    return redirect(url_for('viewfood'))

@app.route('/admin/viewuser')
def viewuser():
    db = shelve.open('databases/user.db', 'r')
    user_dict = {}
    for user_id in db:
        print(db[user_id].get_username())
        user_dict[user_id] = [db[user_id].get_user_profile_pic(), db[user_id].get_username(), db[user_id].get_user_firstname(), db[user_id].get_user_lastname()]
    db.close()
    return render_template('admin/viewuser.html', userlist = user_dict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('loggedin') == True:
        return redirect(url_for('home'))
    else:
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            print("posting")
            db = shelve.open('databases/user.db', 'r')
            username = request.form['username'].lower()
            pw = request.form['password']
            #for loop to check every users in db whether they have the same username and password
            for user in db:
                user = db[user]
                if user.get_username() == username and pbkdf2_sha256.verify(pw, user.get_user_pw()) == True:
                    session['user_id'] = user.get_user_id()
                    session['name'] = user.get_user_fullname()
                    session['username'] = user.get_username()
                    session['profile_pic'] = user.get_user_profile_pic()
                    session['first_name'] = user.get_user_firstname()
                    session['last_name'] = user.get_user_lastname()
                    session['email'] = user.get_user_email()
                    session['cart'] = {}
                    session['loggedin'] = True
                    session['payment'] = False
                    db.close()
                    # #making session['verifying'] by checking if user is inside pendingstaff.db
                    # db = shelve.open('databases/pendingstaff.db')
                    # if session['user_id'] in db:
                    #     session['verifying'] = True
                    # db.close()
                    #checking if user is staff, if so redirect them to the staff interface
                    # staffdb = shelve.open('databases/staff.db','r')
                    # if session['user_id'] in staffdb:
                    #     session['isstaff'] = True
                    # staffdb.close()

                    # try:
                    #     if request.form['remember']:
                    #         session['remember'] = True
                    # except:
                    #     pass
                    #this means that the for loop found a match, and our session data is now in used.
                    return redirect(url_for('home'))
                print("checking")
            #for loops ends and has no match...
            db.close()
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def createUser():
    if session.get('loggedin') == True:
        return redirect(url_for("home"))
    else:
        createUserForm = CreateUserForm(request.form)
        if request.method == 'POST' and createUserForm.validate():
            print("posting")
            email = request.form['email'].lower()
            username = request.form['username'].lower()
            password = request.form['password']
            firstname= request.form['first_name']
            lastname= request.form['last_name']

            #Validating form(if similar)
            if username == password:
                similarerror = 'Username and password cannot be the same'
                return render_template('register.html', form=createUserForm, similarerror=similarerror)

            #retrieving user.db
            db = shelve.open('databases/user.db', 'w')
            if len(db) == 0:
                user = User(email, username, password, firstname, lastname)  # user object
                db[user.get_user_id()] = user
                # testing code
                print("successfully posted")
                db.close()
                return redirect(url_for("home"))
            else:
                for user in db:
                    user = db[user]
                    if user.get_user_email() == email:
                        emailerror = 'This email is in use, please enter another email.'
                        return render_template('register.html', form=createUserForm, emailerror=emailerror)
                    if user.get_username() == username:
                        usernameerror = 'This username is in use, please enter another username.'
                        return render_template('register.html', form=createUserForm, usernameerror=usernameerror)
                    else:
                        db.close()

                        #posting to user.db after no errors
                        db = shelve.open('databases/user.db')
                        user = User(email,username,password,firstname,lastname) #user object
                        db[user.get_user_id()] = user

                        #testing code
                        print("successfully posted")
                        db.close()
                        return redirect(url_for("home"))

    return render_template('register.html', form=createUserForm)

@app.route('/logout')
def logout():
    if session.get('loggedin')==True:
        session.clear()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route('/profile/viewprofile')
def viewprofile():
    return render_template('profile/viewprofile.html')

app.config["PROFILE_PIC_UPLOADS"] = "static/images/profilepictures" #initializiing path for future references
app.config["ALLOWED_PROFILE_PIC_TYPE"] = ["PNG","JPG","JPEG","GIF"]

@app.route('/profile/editprofile', methods = ["GET", "POST"])
def editprofile():
    if session.get('loggedin') != True:
        return redirect(url_for('home'))
    else:
        form = EditForm(request.form)
        db = shelve.open('databases/user.db','w')
        userObj = db[session['user_id']]
        if request.method == 'POST' and form.validate():
            print("posting")
            username = request.form['username']
            userObj.set_username(username)
            session['username'] = username

            first_name = request.form['first_name']
            userObj.set_user_firstname(first_name)
            session['first_name'] = first_name

            last_name = request.form['last_name']
            userObj.set_user_lastname(last_name)
            session['last_name'] = last_name

            email = request.form['email']
            userObj.set_user_email(email)
            session['email'] = email

            db.close()

            if request.files['image'].filename != "":
                image = request.files["image"]
                # our name attribute inside our input form field.  this will return a file object in this case should be image/png
                if not allowed_image(image.filename):
                    extensionerror = "That image extension is not allowed"
                    print(extensionerror)
                    return render_template('/profile/editprofile.html', form=form, extensionerror=extensionerror)
                else:
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["PROFILE_PIC_UPLOADS"], filename))
                    profile_pic = filename
                    session['profile_pic'] = profile_pic
                    db = shelve.open('databases/user.db', 'r')
                    userObj = db[session['user_id']]
                    userObj.set_user_profile_pic(profile_pic)
                    db.close()
            db = shelve.open('databases/user.db', 'w')
            db[session['user_id']] = userObj
            db.close()
            return redirect(url_for('viewprofile'))
        return render_template('profile/editprofile.html', form=form)

@app.route("/profile/orderhistory")
def viewhistory():
    db = shelve.open('databases/orderhistory.db')
    user_id = session['user_id']
    if user_id in db:
        orderlist = db[user_id]
        db.close()
        return render_template('profile/orderhistory.html', foodlist = orderlist)
    else:
        return render_template('profile/orderhistory.html')

@app.route("/profile/orderhistory/<id>", methods=["POST","GET"])
def deletehistory(id):
    order_no = int(id)
    db = shelve.open('databases/orderhistory.db','w')
    user_id = session['user_id']
    tempdb = db[user_id]
    tempdb.pop(order_no)
    db[user_id] = tempdb
    db.close()
    return redirect(url_for('viewhistory'))
# Cart

@app.route("/aston/menu", methods = ["POST","GET"])
def menu():
    db = shelve.open('databases/food.db', 'r')
    food_list = {}
    signature_list = {}
    burger_list = {}
    chicken_list = {}
    side_list = {}
    for item in db:
        category = db[item].get_food_category()
        food_list[db[item].get_name()] = [db[item].get_food_category()]
        if category == "signature":
            signature_list[db[item].get_name()] = [db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
        elif category == "burger":
            burger_list[db[item].get_name()] = [db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
        elif category == "chicken":
            chicken_list[db[item].get_name()] = [db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
        elif category == "side":
            side_list[db[item].get_name()] = [db[item].get_description(), "{:.2f}".format(db[item].get_price()), db[item].get_picture()]
    db.close()

    if request.method == "POST":
        if session.get('loggedin') != True:
            return redirect(url_for('login'))
        else:
            item = request.form['add_cart'].split(',')
            name = item[0]
            cost = "{:.2f}".format(float(item[1]))
            db = shelve.open('databases/food.db', 'r')
            picture = db[name].get_picture()
            db.close()
            if session['cart'].get(name):
                session['cart'][name][1] += 1
                session['cart'][name][2] = "{:.2f}".format(float(session['cart'][name][1]) * float(session['cart'][name][0]))
            else:
                session['cart'][name] = [cost, 1, cost, picture]
            flash('has been added', name)
    return render_template('aston/menu.html', form= form, foodlist=food_list, signaturelist=signature_list, burgerlist=burger_list, chickenlist=chicken_list, sidelist=side_list)


@app.route("/aston/cart", methods=["POST","GET"])
def viewcart():
    sub_total = 0
    delivery = "{:.2f}".format(4)

    for item in session['cart']:
        sub_total += float(session['cart'][item][2])
    sub_total = "{:.2f}".format(sub_total)
    total_cost = "{:.2f}".format(float(delivery) + float(sub_total))

    return render_template('aston/cart.html', sub_total=sub_total, delivery=delivery, total_cost=total_cost)

@app.route("/aston/cart/<action>", methods=["POST","GET"])
def editcart(action):
    if action == "plus":
        name = request.form["add_item"]
        cart = session['cart']
        quantity = cart[name][1]
        quantity += 1
        cart[name][1] = quantity
        item_price = float(cart[name][0]) * float(cart[name][1])
        cart[name][2] = "{:.2f}".format(item_price)
        session['cart'] = cart

    if action == "minus":
        name = request.form.get("minus_item")
        cart = session['cart']
        quantity = cart[name][1]
        if quantity > 1:
            quantity -= 1
            cart[name][1] = quantity
            item_price = float(cart[name][0]) * float(cart[name][1])
            cart[name][2] = "{:.2f}".format(item_price)
        else:
            cart[name][1] = 1
            cart[name][2] = cart[name][0]
        session['cart'] = cart

    return redirect(url_for('viewcart'))



@app.route("/aston/carts/<id>", methods = ["POST"])
def deleteitem(id):
    cart = session['cart']
    cart.pop(id)
    session['cart'] = cart
    return redirect(url_for('viewcart'))

@app.route("/aston/payment", methods =["GET","POST"])
def payment():
    paymentform = Payment(request.form)
    if len(session['cart']) != 0:
        db = shelve.open("databases/user.db", 'w')
        if request.method == "POST" and paymentform.validate():
            block_no = request.form['block_number']
            postal_code = request.form['postal_code']
            cardnumber = request.form['cardnumber']
            expirydate = request.form['expirydate']
            security = request.form['security']
            try:
                int(cardnumber)
                if expirydate[2] == '/':
                    expirydate.replace('/', '')
                    try:
                        expiry = expirydate.replace('/', '')
                        int(expiry)

                        if int(expiry[0] + expiry[1]) <= 12:
                            try:
                                int(security)
                                user_id = session['user_id']
                                user = db[user_id]
                                user.set_block_number(block_no)
                                user.set_postal_code(postal_code)
                                db.close()

                                session['payment'] = True
                                db = shelve.open('databases/orderhistory.db', 'w')
                                count = 1
                                user_id = session['user_id']

                                if len(db) == 0 or user_id not in db:
                                    db[user_id] = {1: session['cart']}
                                else:
                                    orderlist = db[user_id]
                                    for number in orderlist:
                                        if count == int(number):
                                            count += 1
                                    cart = session['cart']
                                    orderlist[count] = cart
                                    db[user_id] = orderlist
                                db.close()
                                return redirect(url_for('receipt'))
                            except:

                                error = 'CVV should be 3 digits.'
                                return render_template("aston/payment.html", form=paymentform, securityerror=error)
                        else:
                            error = 'Month has to be 0-12.'
                            return render_template("aston/payment.html", form=paymentform, expiryerror=error)
                    except:
                        error = 'Expiry Date must be in the format of mm/yy.'
                        return render_template("aston/payment.html", form=paymentform, expiryerror=error)
                else:
                    error = 'Expiry Date must be in the format of mm/yy.'
                    return render_template("aston/payment.html", form=paymentform, expiryerror=error)
            except:
                error = 'Card number must be 16 digits.'
                return render_template("aston/payment.html", form=paymentform, cardnumbererror=error)

        return render_template("aston/payment.html", form=paymentform)
    else:
        return redirect(url_for('viewcart'))

@app.route('/aston/receipt', methods=["GET","POST"])
def receipt():
    sub_total = 0
    delivery = "{:.2f}".format(4)
    if session['payment']:
        for item in session['cart']:
            sub_total += float(session['cart'][item][2])
        sub_total = "{:.2f}".format(sub_total)
        total_cost = "{:.2f}".format(float(delivery) + float(sub_total))
        session['payment'] = False
        session['cart'] = {}

        if request.method == "POST":
            return redirect(url_for('aston'))

        return render_template('aston/receipt.html', sub_total=sub_total, delivery=delivery, total_cost=total_cost)
    else:
        session['payment'] = False
        return redirect(url_for('viewcart'))


# Seating Plan

"""@app.route("/seatplan")
def seatplan():
    return render_template("temporary.html")"""

"""@app.route("/temporary")
def temporary():
    return render_template("temporary.html")"""

@app.route("/reserveseat", methods=["GET", "POST"])
def reserveseat():
    select = SeatForm(request.form)
    if request.method == 'POST' and select.validate():
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'c')

        try:
            guest_dict = db['Seats']
        except:
            print('Error in retrieving Seats from guest_storage.db')

        seat = Seat(select.name.data, select.time.data, select.seat.data)
        guest_dict[seat.get_user_id()] = seat
        db['Seats'] = guest_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('temporary.html', form=select) #error: had to change form=SeatForm to select instead
                                                          #need to pop out a confirmation screen+shelve

@app.route('/retrieveSeats')
def retrieve_seats():
    guest_dict = {}
    db = shelve.open('databases/guest_storage.db', 'r')
    guest_dict = db['Seats']
    db.close()

    guest_list = []
    for key in guest_dict:
        seat = guest_dict.get(key)
        guest_list.append(seat)

    return render_template('retrieveSeats.html', count=len(guest_list), guest_list=guest_list)
# @app.route('/retrieveOneGuest/<int:id>'):
# def RetrieveSingleGuest(id):
# guest = GuestModel.query.filter_by(user_id=id).first()
#if guest:
#    return render_template('retrieve_seats.html', guest=guest)

@app.route("/updateSeats/<id>/", methods=['GET', 'POST'])
def update_seats(id):
    update_seats = SeatForm(request.form)
    if request.method == 'POST' and update_seats.validate():
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'w')
        guest_dict = db['Seats']

        seat = guest_dict.get(id)
        seat.set_name(update_seats.name.data)
        seat.set_seat(update_seats.seat.data)

        db['Seats'] = guest_dict
        db.close()

        return redirect(url_for('retrieve_seats'))
    else:
        guest_dict = {}
        db = shelve.open('databases/guest_storage.db', 'r')
        guest_dict = db['Seats']
        db.close()

        seat = guest_dict.get(id)
        update_seats.name.data = seat.get_name()
        update_seats.seat.data = seat.get_seat()

        return render_template("updateSeats.html", form = update_seats)

@app.route('/deleteSeats/<id>', methods=['POST'])
def delete_seats(id):
    guest_dict = {}
    db = shelve.open('databases/guest_storage.db', 'w')
    guest_dict = db['Seats']

    guest_dict.pop(id)

    db['Seats'] = guest_dict
    db.close()

    return redirect(url_for('retrieve_seats'))



# Staff Temperature record

@app.route("/staff/morning", methods=['GET', 'POST'])
def create_morning():
    m_tem = TemperatureMorning(request.form)
    if request.method == 'POST' and m_tem.validate():
        db = shelve.open('databases/temperature.db', 'w')
        morning = request.form['temperature_morning']
        afternoon = request.form['temperature_afternoon']
        night = request.form['temperature_night']
        name = request.form['username']
        declaration_1 = request.form['declaration_1']
        declaration_2 = request.form['declaration_2']
        declaration_3 = request.form['declaration_3']
        declaration_4 = request.form['declaration_4']
        print(declaration_1)
        staff = TemperatureM(morning, afternoon, night, name, declaration_1, declaration_2, declaration_3, declaration_4)
        db[name] = staff
        db.close()
    return render_template("staff/morningtemp.html", form=m_tem)

@app.route('/staff/retrievetemps')
def retrieve_temps():
    db = shelve.open('databases/temperature.db', 'r')
    temp = {}
    for name in db:
        print(name)
        morningtemp = db[name].get_temperaturemorning()
        temp[name] = morningtemp
    db.close()
    return render_template('staff/temperature log morning.html', templist=temp)

if __name__ == '__main__':
    app.run(debug=True)
