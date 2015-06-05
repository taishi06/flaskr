import MySQLdb


def connect(db_name):
	try:
		return MySQLdb.connect(host='localhost', user='root', passwd='t3rt3r06', db=db_name)
	except Exception as e:
		return str(e)
