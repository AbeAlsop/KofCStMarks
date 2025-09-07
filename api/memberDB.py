import sqlite3
import secrets

db_name = 'kofc.db'

def execute(command, parameters):
	with sqlite3.connect(db_name) as con:
		cur = con.cursor()
		cur.execute(command, parameters)
		con.commit()

def query(query, parameters):
	with sqlite3.connect(db_name) as con:
		cur = con.cursor()
		return cur.execute(query, parameters).fetchall()


# id: K of C membership number
# first, middle, last: name
# degree: integer 1-4
# council, city, state: local council
# date: membership expiration as "YYYY-MM-DD"
def insert_member(id, first, middle, last, degree, council, city, state, date):
	token = secrets.token_urlsafe(24)
	cmd = "INSERT INTO members (member_id,token,first_name,middle_name,last_name,degree,council,city,state,dues_paid_date) VALUES (?,?,?,?,?,?,?,?,?,?)"
	execute(cmd, (id,token,first,middle,last,degree,council,city,state,date))

# id: K of C membership number
def get_member_by_number(id):
	res= query("SELECT * FROM members WHERE member_id=?", (id,))
	if len(res) < 1:
		raise Exception(f"Member {id} not found")
	return res[0]

def get_member_by_token(token):
	res= query("SELECT * FROM members WHERE token=?", (token,))
	if len(res) < 1:
		raise Exception("The token provided is not valid")
	return res[0]


def populate_test_data():
	insert_member(23456,'Abraham','D','Alsop',3,12172,'Boise','ID','2025-12-31')

if __name__ == "__main__":
	print(get_member_by_number(23456))


