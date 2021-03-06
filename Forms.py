from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import *

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField('Email', [validators.Length(min=1,
                                                    max=150), validators.DataRequired(), validators.email()])
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired(),
                                          EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired()])
    remember = BooleanField('Remember me')