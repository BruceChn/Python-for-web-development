from flask_wtf import Form
from wtforms import StringField,DateField,IntegerField,SelectField
from wtforms.validators import DataRequired

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