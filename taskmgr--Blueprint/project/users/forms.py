from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Length,EqualTo,Email

class RegisterForm(Form):
	name = StringField('UserName',validators = [DataRequired(),Length(min = 6,max = 25)])
	email = StringField('Email',validators = [DataRequired(),Email(),Length(min = 6,max = 25)])
	password = PasswordField('Password',validators = [DataRequired(),Length(min = 6,max = 25)])
	confirm = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password',message = 'Password must Match')])
	
class LoginForm(Form):
	name = StringField('Username',validators = [DataRequired()])
	password = PasswordField('Password',validators = [DataRequired()])