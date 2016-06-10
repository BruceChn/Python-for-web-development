from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import Flask,flash,redirect,render_template,request,session, url_for,g
from forms import AddTaskForm,RegisterForm,LoginForm
from sqlalchemy.exc import IntegrityError
import datetime


app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)
from models import Task,User

def login_required(func):
	@wraps(func)
	def wrap(*args, **argv):
		if 'logged_in' in session:
			return func(*args, **argv)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

#route handlers
@app.route('/logout/') 
def logout():
	session.pop('logout',None)
	session.pop('user_id',None)
	flash('Goodbye')
	return redirect(url_for('login'))
@app.route('/',methods = ['GET','POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by(name = request.form['name']).first()
			if user is not None and user.password == request.form['password']:
				session['login_in'] = True
				session['user_id'] = user.id
				flash('Welcome')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid username or password'
		else:
			flash("Both fields are required")
	return render_template('login.html',form = form, error = error)
@app.route('/task')
@login_required
def tasks():

	return render_template(
		'task.html',
		form = AddTaskForm(request.form),
		open_tasks = open_tasks(),
		closed_tasks = closed_tasks()
	)

def open_tasks():
	return db.session.query(Task).filter_by(status = 1, user_id = session['user_id']).order_by(Task.due_date.asc())

def closed_tasks():
	return db.session.query(Task).filter_by(status = 0, user_id = session['user_id']).order_by(Task.due_date.asc())

@app.route('/add',methods = ['GET','POST'])
@login_required
def new_task():
	error = None
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(form.name.data,
							form.due_date.data,
							form.priority.data,
							datetime.datetime.utcnow(),
							'1',
							session['user_id'])
			db.session.add(new_task)
			db.session.commit()
			flash('new entry was successfully posted. Thansk.!')
			return redirect(url_for('tasks'))
	return  render_template('task.html',
							form = form,
							error = error,
							open_tasks = open_tasks(),
							closed_tasks = closed_tasks())
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id = new_id).update({"status":"0"})
	db.session.commit()
	flash('The task was marked as complete')
	return redirect(url_for('tasks'))
	
@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
	id = task_id
	db.session.query(Task).filter_by(task_id = id).delete()
	db.session.commit()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))

@app.route('/register',methods = ['GET','POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data
			)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('Thanks for registering.Please login in')
				return redirect(url_for('login'))
			except IntegrityError:
				error = 'That username and/or emial already exist'
	return render_template('register.html',form = form,error = error)

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s filed - %s" % (getattrr(form, field).label.text,error),'error')