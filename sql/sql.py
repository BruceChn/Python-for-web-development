import sqlite3

with sqlite3.connect("new.db") as conn:

	c = conn.cursor()
	
	sql = {'average': "Select avg(population) From population",
			'maximum': "Select max(population) From population",
			'minimun': "select min(population) From population",
			'sum': "Select sum(population) From population",
			'count':"Select count(city) From population Where state = 'CA'"}
	for key,val in sql.items():
		c.execute(val)
		
		row = c.fetchone()
		
		print key , row[0]
	
	
conn.close()