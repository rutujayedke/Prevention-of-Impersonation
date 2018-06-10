import MySQLdb
conn = MySQLdb.connect (host = "localhost",user = "root", passwd = "roshan", db = "login")
cursor = conn.cursor ()
row = cursor.fetchone ()
while row != None:
	print( "user-name:", row[0], "\tpassword", row[1])
	row = cursor.fetchone ()
cursor.close ()
conn.close ()
