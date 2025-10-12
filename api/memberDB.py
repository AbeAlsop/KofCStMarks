import sqlite3
import secrets
import json
from dataclasses import dataclass, asdict

db_name = 'kofc.db'

@dataclass
class Member:
	member_id: int
	first_name: str
	middle_name: str
	last_name: str
	degree: int
	council: int
	city: str
	state: str
	dues_date: str
	def __init__(self, record):
		self.member_id= record[0]
		self.first_name= record[2]
		self.middle_name= record[3]
		self.last_name= record[4]
		self.degree= record[5]
		self.council= record[6]
		self.city= record[7]
		self.state= record[8]
		self.dues_date= record[9]
	def toJSON(self):
		return json.dumps(asdict(self))


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
	cmd = """INSERT INTO members
		(member_id,token,first_name,middle_name,last_name,degree,council,city,state,dues_paid_date)
		VALUES (?,?,?,?,?,?,?,?,?,?)
		ON CONFLICT(member_id) DO UPDATE SET 
		first_name=excluded.first_name,middle_name=excluded.middle_name,last_name=excluded.last_name,degree=excluded.degree,council=excluded.council,city=excluded.city,state=excluded.state,dues_paid_date=excluded.dues_paid_date"""
	execute(cmd, (id,token,first,middle,last,degree,council,city,state,date))

# id: K of C membership number
def get_member_by_number(id):
	res= query("SELECT member_id,token,first_name,middle_name,last_name,degree,council,city,state,dues_paid_date FROM members WHERE member_id=?", (id,))
	if len(res) < 1:
		raise Exception(f"Member {id} not found")
	return Member(res[0])

def get_member_by_token(token):
	res= query("SELECT member_id,token,first_name,middle_name,last_name,degree,council,city,state,dues_paid_date FROM members WHERE token=?", (token,))
	if len(res) < 1:
		raise Exception("The token provided is not valid")
	return Member(res[0])


def create_db():
	cmd = """CREATE TABLE IF NOT EXISTS members (
		member_id INTEGER PRIMARY KEY,
		token TEXT UNIQUE,
		first_name TEXT,
		middle_name TEXT,
		last_name TEXT,
		degree INTEGER,
		council INTEGER,
		city TEXT,
		state TEXT,
		dues_paid_date TEXT);"""
	execute(cmd, ())

def populate_test_data():
	insert_member(23456,'Abraham','D','Alsop',3,12172,'Boise','ID','2025-12-31')

if __name__ == "__main__":
	create_db()
	populate_test_data()
	member= get_member_by_number(23456)
	print(member.toJSON())


