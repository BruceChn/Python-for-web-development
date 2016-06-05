import sqlite3

with sqlite3.connect("newnum.db") as conn:
	
	c = conn.cursor()
	
	prompt = """
	Select the operation you want to perform: """
	
	while True:
		x = raw_input(prompt)
		
		if x in set(["1","2","3","4"]):
			operation = {1:"avg", 2:"max", 3:"min", 4:"sum"}[int(x)]
			c.execute("select {}(num) from NUMS".format(operation))
			get = c.fetchone()
			
			print operation + ": {:f}".format(get[0])
		else:
			exit()