import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as conn:
	c = conn.cursor()
	
	c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTERGER NOT NULL, status INTERGER NOT NULL)""")
	
	c.execute("""INSERT INTO tasks (name, due_date, priority, status)
			Values("Finish this tutorial","03/25/2015",10,1)""")
	c.execute("""INSERT INTO tasks (name,due_date,priority,status) 
			Values("do some thing awsome","05/24/2016",10,1)""")
	