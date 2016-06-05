import sqlite3

with sqlite3.connect("blog.db") as conn:
	c = conn.cursor()
	
	c.execute("Create Table posts(title TEXT,post TEXT)")
	
	c.execute('Insert Into posts Values("good","I\'m good")')
	c.execute('Insert Into posts Values("Well","I\'m well.")')
conn.close()