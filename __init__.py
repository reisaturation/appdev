from flask import Flask, render_template, request, redirect, url_for, session
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

@app.route("/home")
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
                    session['loggedin'] = True
                    db.close()
                    # #making session['verifying'] by checking if user is inside pendingstaff.db
                    # db = shelve.open('databases/pendingstaff.db')
                    # if session['user_id'] in db:
                    #     session['verifying'] = True
                    # db.close()
                    #checking is user is staff, if so redirect them to the staff interface
                    # staffdb = shelve.open('databases/staff.db','r')
                    # if session['user_id'] in tutordb:
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

            return redirect(url_for('viewprofile'))
        return render_template('profile/editprofile.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
