from flask_wtf import Form
from wtforms import StringField,DateField,IntegerField,SelectField,PasswordField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class AddTaskForm(Form):
	task_id = IntegerField()
	name = StringField('Task name', validators = [DataRequired()])
	due_date = DateField(
		'Due Date(mm/dd/yyyy)',
		validators = [DataRequired()],format = '%m/%d/%Y')
	priority = SelectField(
		'Priority',
		validators = [DataRequired()],choices = [('1','1'),('2','2'),('3','3'),('4','4')])
	status = IntegerField('Status')
	
class RegisterForm(Form):
	name = StringField('UserName',validators = [DataRequired(),Length(min = 6,max = 25)])
	email = StringField('Email' ,validators = [DataRequired(),Email()])
	password = PasswordField('Password',validators = [DataRequired(), Length(min = 6,max = 40)])
	confirm = PasswordField('Repeat Password', validators = [DataRequired(),EqualTo('password',message = 'Password Must Match')])

class LoginForm(Form):
	name = StringField('Username',validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])