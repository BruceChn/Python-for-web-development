from views import db
from models import Task
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

db.session.add(Task("Finish the tutorial",date(2015,3,13),4,1))
db.session.add(Task("move",date(2016,6,14),1,1))

db.session.commit()
