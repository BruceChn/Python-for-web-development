import os
import unittest

from project import app,db,bcrypt
from project._config import basedir
from project.models import User,Task

TEST_DB = 'test.db'

class AllTESTS(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		app.config['Debug'] = False
		self.app = app.test_client()
		db.create_all()
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()
	
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)
		
	def login(self,name,password):
		
		return self.app.post('/',data = dict(name = name, password=password),follow_redirects = True)
	
	def register(self,name,email,password,confirm):
		return self.app.post('/register',data = dict(name = name,email = email,password = password,confirm = confirm),follow_redirects = True)
		

	
	
	def logout(self):
		return self.app.get('/logout',follow_redirects = True)
	
	def test_logged_in_users_can_logout(self):
		self.register('Fletch','wsdf@gmail.com','python101','python101')
		self.login('Fletch','python101')
		response = self.logout()
		self.assertIn(b'Goodbye',response.data)
	
	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		assert 'Goodbye' not in response.data 
	
	def test_user_setup(self):
		new_user = User("michael","michael@mherman.org","michaelherman")
		db.session.add(new_user)
		db.session.commit()
	
	def test_users_can_register(self):
		new_user = User("Michael","micheal@mherman.org","michaelherman")
		
		db.session.add(new_user)
		db.session.add(new_user)
		db.session.commit()
		
		test = db.session.query(User).all()
		
		for t in test:
			assert t.name == "Michael"
		
	def test_form_is_present_on_login_page(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		assert "access your task list" in response.data
		
	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo','bar')
		assert 'Invalid username' in response.data
	
	def test_registered_user_can_login(self):
		self.register('Michael','michael@google.com','python','python')
		response = self.login('Michael','python')
		assert 'Welcome' in response.data
	
	def test_form_is_present_on_register_page(self):
		response = self.app.get('/register')
		self.assertEqual(response.status_code,200)
		assert 'Please register to access the task list' in response.data
	
	def test_user_registeration(self):
		self.app.get('/register', follow_redirects = True)
		response = self.register('Michael', 'michael@realpython.com', 'python', 'python')
		assert 'Thanks' in response.data
		
	def test_user_registeration_error(self): #register a username which is already used
		self.app.get('/register',follow_redirects = True)
		self.register('Michael','michael@realpython.com','python','python')
		self.app.get('/register',follow_redirects = True)
		response = self.register('Michael','michael@realpython.com','python','python')
		assert 'already exist' in response.data
		
	def test_logged_in_users_can_logout(self):
		self.register('Fletch','fletch@gmail.com','python','python')
		self.login('Fletch','python')
		response = self.logout()
		assert 'Goodbye' in response.data
	
	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		assert 'Goodbye' not in response.data
	
	def test_logged_in_users_can_access_tasks_page(self):
		self.register('Michael','michael@google.com','python','python')
		self.login('Michael','python')
		response = self.app.get('/tasks')
		self.assertEqual(response.status_code,200)
		assert 'Add a new task' in response.data
		
	def test_not_logged_in_users_cannot_access_tasks_page(self):
		response = self.app.get('/tasks', follow_redirects = True)
		assert 'You need to login first' in response.data
		
	def create_user(self,name,email,password):
		new_user = User(name = name,email = email,password = bcrypt.generate_password_hash(password))
		db.session.add(new_user)
		db.session.commit()
	
	def create_task(self):
		return self.app.post('/add', data = dict(name = "goto the back",due_date = '02/05/2016',priority = '1',posted_date = '02/04/2014',status = '1'),follow_redirects = True)
	
	def test_users_can_add_task(self):
		self.create_user('Michael','michael@realypython.com','python')
		self.login('Michael','python')
		self.app.get('/tasks',follow_redirects = True)
		response = self.create_task()
		assert 'successfully' in response.data
	
	def test_users_cannot_add_tasks_when_error(self):
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks', follow_redirects=True)
		response = self.app.post('/add', data=dict(
		name='Go to the bank',
		due_date='',
		priority='1',
		posted_date='02/05/2014',
		status='1'
		), follow_redirects=True)
		self.assertIn(b'enter the correct date', response.data)
		
	def test_users_can_complete_tasks(self):
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks', follow_redirects=True)
	
		self.create_task()
		response = self.app.get("/complete/1", follow_redirects=True)
		self.assertIn(b'complete', response.data)
	
	def test_users_can_delete_tasks(self):
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks', follow_redirects=True)
		self.create_task()
		test = db.session.query(Task).all()
		response = self.app.get('/delete/1', follow_redirects=True)
		self.assertIn(b'The task was deleted.', response.data)
		
	def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user('Fletcher', 'fletcher@realpython.com','python101')
		self.login('Fletcher', 'python101')
		self.app.get('/tasks', follow_redirects=True)
		response = self.app.get("/complete/1", follow_redirects=True)
		self.assertNotIn( b'The task is complete. Nice.', response.data)
		self.assertIn(b'You can only update tasks that belong to you.',response.data)
	
	def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
		self.create_user('Michael', 'michael@realpython.com', 'python')
		self.login('Michael', 'python')
		self.app.get('/tasks', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user('Fletcher', 'fletcher@realpython.com','python101')
		self.login('Fletcher', 'python101')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get("/delete/1", follow_redirects=True)
		self.assertNotIn( b'The task was deleted.', response.data)
		self.assertIn(b'You can only delete tasks that belong to you.',response.data)
	
	def test_default_user_role(self):
		db.session.add(
			User("Johnny","john@doe.com","python")
		)
		users = db.session.query(User).all()
		for user in users:
			self.assertEquals(user.role,'user')
			
	def create_admin_user(self):
		new_user = User(
			name = 'Superman',
			email = 'admin@realpython.com',
			password = bcrypt.generate_password_hash('allpowerful'),
			role = 'admin'
		)
		db.session.add(new_user)
		db.session.commit()
	
	def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
		self.create_user('Michael','zhdsfkl@gmail.com','python')
		self.login('Michael','python')
		self.app.get('/tasks',follow_redirects = True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		self.login('Superman','allpowerful')
		self.app.get('/tasks',follow_redirects = True)
		response = self.app.get("/delete/1",follow_redirects = True)
		
		self.assertNotIn(b'You can only delete tasks that belong to you',response.data)
		
	def test_task_template_displays_logged_in_user_name(self):
		self.register('Zhenwei','zhenwei@gmail.com','python','python')
		self.login('Zhenwei','python')
		response = self.app.get('/tasks',follow_redirects = True)
		self.assertIn(b'Zhenwei',response.data)
	
	def test_404_error(self):
		response = self.app.get('/this-route-doen')
		self.assertEquals(response.status_code,404)
		self.assertIn(b'Go back Home',response.data)
		
if __name__ == "__main__":
		unittest.main()