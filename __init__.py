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

@app.route("/aston")
def aston():
    return render_template("aston.html")

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
                    db.close()
                    # #making session['verifying'] by checking if user is inside pendingstaff.db
                    # db = shelve.open('databases/pendingstaff.db')
                    # if session['user_id'] in db:
                    #     session['verifying'] = True
                    # db.close()
                    #checking is user is staff, if so redirect them to the staff interface
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

# Cart

@app.route("/aston/menu")
def menu():
    return render_template('astonmenu/menu.html')


@app.route("/aston/menu/signature", methods = ["POST","GET"])
def signature():
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
    return render_template('astonmenu/signature.html', form= form)


@app.route("/aston/menu/burger")
def burger():
    return render_template('astonmenu/burger.html')

@app.route("/aston/menu/chicken")
def chicken():
    return render_template('astonmenu/chicken.html')

@app.route("/aston/menu/sidedish")
def sidedish():
    return render_template('astonmenu/sidedish.html')

@app.route("/aston/cart", methods=["POST","GET"])
def viewcart():
    sub_total = 0
    delivery = "{:.2f}".format(4)

    if request.method == "POST":
        for item in session['cart']:
            if request.form.get("add_item"):
                quantity = int(request.form.get("add_item"))
                quantity += 1
                session['cart'][item][1] = quantity
                item_price = float(session['cart'][item][0]) * float(session['cart'][item][1])
                session['cart'][item][2] = "{:.2f}".format(item_price)

            if request.form.get("minus_item"):
                quantity = int(request.form.get("minus_item"))
                if quantity > 1:
                    quantity -= 1
                    session['cart'][item][1] = quantity
                    item_price = float(session['cart'][item][0]) * float(session['cart'][item][1])
                    session['cart'][item][2] = "{:.2f}".format(item_price)
                else:
                    session['cart'][item][1] = 1
                    session['cart'][item][2] = session['cart'][item][0]

    for item in session['cart']:
        sub_total += float(session['cart'][item][2])
    sub_total = "{:.2f}".format(sub_total)
    total_cost = "{:.2f}".format(float(delivery) + float(sub_total))

    return render_template('astonmenu/cart.html', sub_total=sub_total, delivery=delivery, total_cost=total_cost)


@app.route("/aston/cart/<id>", methods = ["POST"])
def deleteitem(id):
    cart = session['cart']
    cart.pop(id)
    session['cart'] = cart
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

        seat = Seat(select.name.data, select.seat.data)
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


@app.route("/updateSeats/<int:id>/", methods=['GET', 'POST'])
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

@app.route('/deleteSeats/<int:id>', methods=['POST'])
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
        temps_dict = {}
        db = shelve.open('databases/temperature.db', 'w')
        try:
            temps_dict = db['temps']
        except:
            print("Error in retrieving temperature from temperature.db.")
        temperature_m = TemperatureM(m_tem.temperature_morning.data)
        temps_dict[temperature_m.get_temperaturemorning()] = temperature_m
        db['temps'] = temps_dict
        print(db['temps'])
        db.close()

    return render_template("staff/morningtemp.html", form=m_tem)

@app.route('/staff/retrievetemps')
def retrieve_temps():
    temps_dict = {}
    db = shelve.open('databases/temperature.db', 'r')
    temps_dict = db['temps']
    db.close()

    temps_list = []
    for key in temps_dict:
        temps_list.append(key)

    return render_template('staff/temperature log morning.html', count=len(temps_list), temps_list=temps_list)

if __name__ == '__main__':
    app.run(debug=True)
