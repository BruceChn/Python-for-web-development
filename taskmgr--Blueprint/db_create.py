from project import db,bcrypt
from project.models import Task,User

from datetime import date

###with sqlite3.connect(DATABASE_PATH) as conn:
#	c = conn.cursor()
	
#	c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
#	name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTERGER NOT NULL, status INTERGER NOT NULL)""")
	
#	c.execute("""INSERT INTO tasks (name, due_date, priority, status)
#			Values("Finish this tutorial","03/25/2015",10,1)""")
#	c.execute("""INSERT INTO tasks (name,due_date,priority,status) 
#			Values("do some thing awsome","05/24/2016",10,1)""")


db.create_all()
db.session.add(User("admin","admin@gmail.com",bcrypt.generate_password_hash("admin"),"admin"))
db.session.add(Task("Finish this tutorial", date(2015, 3, 13), 1, date(2015,2, 13), 1, 1))

db.session.add(Task("move",date(2016,6,14),1,date(2016,6,13),1,1))

db.session.commit()

