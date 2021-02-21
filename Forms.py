from wtforms import *
from wtforms.validators import *

class AdminForm(Form):
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8
                                                            ), validators.DataRequired()])
    code = PasswordField('Code:', [validators.Length(max=150
                                                        ), validators.DataRequired()])

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

class EditForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField('Email', [validators.Length(min=1,
                                                    max=150), validators.DataRequired(), validators.email()])
    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])

class Payment(Form):
    block_number = StringField('Block Number:', [validators.Length(min=1, max=150), validators.DataRequired()])
    postal_code = StringField('Postal Code:', [validators.Length(min=6, max=6), validators.DataRequired()])
    cardnumber = StringField('Card Number:', validators=[length(min=16, max=16), DataRequired()])
    expirydate = StringField('Expiry Date:', validators=[Length(min=5, max=5), DataRequired()])
    security = StringField('CVV:',validators=[length(min=3, max=3), DataRequired()])
    card = SelectField ('Card:', choices=[('MasterCard', 'MasterCard'), ('Nets', 'Nets'), ('PayPal', 'PayPal'), ('Visa', 'Visa')],
                       render_kw={'placeholder': "Card Choice"})
class FoodForm(Form):
    food_name = StringField('Food Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    food_description = StringField('Food Description:', [validators.Length(min=1), validators.DataRequired()])
    food_price = StringField('Food Price:', [validators.Length(min=1, max=150), validators.DataRequired()])
    food_category = SelectField('Category', [validators.DataRequired()],
                                choices=[('', 'Select'), ('signature', 'Signature'), ('chicken', 'Chicken'),
                                         ('side', 'Side Dish'), ('burger', 'Burger')], default='')

class Reviews(Form):
    review = StringField('', [validators.Length(min=1)])


class SeatForm(Form):
    seat = SelectField('Choose your seat here: ',
                       choices=[('1A', '1A'), ('1B', '1B'), ('2A', '2A'), ('2B', '2B'), ('3A', '3A'), ('3B', '3B'),
                                ('4A', '4A'), ('4B', '4B'), ('5A', '5A'), ('5B', '5B'), ('6A', '6A'), ('6B', '6B'),
                                ('7', '7'),
                                ('8', '8'),
                                ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
                                ('15', '15'),
                                ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                                ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26')], default='1A')

    time = SelectField('Choose your timing: ', choices=[('12pm', '12pm'), ('1pm', '1pm'), ('2pm', '2pm'),
                                                        ('3pm', '3pm'), ('4pm', '4pm')], default='')
    name = StringField('Name: ', [validators.Length(min=1, max=150), validators.DataRequired()])

class TemperatureMorning(Form):
    temperature_morning = StringField('Morning Temperature', [validators.DataRequired()])

    temperature_afternoon = StringField('Afternoon Temperature', [validators.DataRequired()])

    temperature_night = StringField('Night Temperature', [validators.DataRequired()])

    username = StringField('Username', [validators.Length(min=8
                                                          ), validators.DataRequired()])

    declaration_1 = RadioField('Are you currently serving Quarantine Order (QO), Leave of Absence (LOA) or Stay-Home Notice (SHN)?' , choices=[('Y', 'Yes'), ('N', 'No')], default='N')

    declaration_2 = RadioField('Within the last 14 days, have you had contact with a COVID-19 (Coronavirus Disease 2019) confirmed case or suspect case, or a person issued Quarantine Order (QO) / Leave of Absence (LOA) / Stay-Home Notice (SHN)?', choices=[('Y', 'Yes'), ('N', 'No')], default='N')

    declaration_3 = RadioField('Within the last 14 days, have you had contact with a member in the household who is unwell?', choices=[('Y', 'Yes'), ('N', 'No')], default='N')

    declaration_4 = RadioField('Are you feeling unwell or having any symptoms (such as fever, cough, muscle ache, joint pain, headaches, sore throat, runny nose, shortness of breath, change in smell, change in taste, diarrhoea)?', choices=[('Y', 'Yes'), ('N', 'No')], default='N')