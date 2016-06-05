import sqlite3
import random

with sqlite3.connect("newnum.db") as conn:
	
	c = conn.cursor()
	
	#c.execute("""Create Table NUMS(num int)""")

	for i in range(100):
		c.execute("Insert Into NUMS Values(?)",(random.randint(0,100),))