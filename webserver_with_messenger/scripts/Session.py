
import html
from UserAccountVerifySet import UserAccount
import sqlite3
import secrets
import os
import re
import time

TIMEOUT = 100

class Session: 
	conn = sqlite3.connect("database.db")
	conn.executescript("""
create table if not exists Sessions (
	ID Integer primary key autoincrement, 
	secret Text unique, 
	acc_id Integer,
	time Integer, 
	foreign key (acc_id) references UserAccountSet (ID)
)
"""	)
	conn.commit()

	ID = None
	match = re.compile("SESSION=(\\S+)").match(os.environ["HTTP_COOKIE"])
		
	if match is None: 
		ID = None
	else: 
		cursor = conn.cursor()
		res = cursor.execute("""
select ID, time 
from Sessions 
where secret = ?
"""		, (match.group(1), )).fetchone()
		cursor.close()

		if res is not None and time.time() - int(res[1]) < TIMEOUT: 
			ID = res[0]
		else: 
			ID = None
			

	def __init__(self, ID): 
		self.conn = sqlite3.connect("database.db")
		self.ID = ID


	def __del__(self): 
		self.conn.close()


	@classmethod
	def get_session(cls): 
		if cls.ID is not None: 
			return cls(cls.ID)
		else: 
			return None


	def update(self):
		self.conn.execute("""
update Sessions 
set secret = ?, 
time = ?
where ID = ?
"""		, (secrets.token_urlsafe(), time.time(), self.ID, ))
		self.conn.commit()


	@classmethod
	def login(cls, mail, pwd): 
		user = UserAccount.get_account(mail)
		
		if user is None or not user.check_password(pwd): 
			return None

		cursor = cls.conn.cursor()
		res = cursor.execute("""
insert into Sessions 
(secret, acc_id, time) 
values (?, ?, ?)
"""		, (secrets.token_urlsafe(), user.ID, time.time(), ))
		cls.conn.commit()
		cursor.close()
		self = cls(res.lastrowid)

		self.output_headers()

		return self
	

	@property
	def secret(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select secret 
from Sessions 
where ID = ?
"""		, (self.ID, )).fetchone()

		if res is None: 
			return None

		cursor.close()

		return res[0]


	def logout(self): 
		self.conn.execute("""
delete from Sessions 
where ID = ?
"""		, (self.ID, ))
		self.conn.commit()


	def output_headers(self): 
		html.add_header("Set-Cookie: SESSION=" + self.secret)


	def get_account_id(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select acc_id 
from Sessions 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return None

		return res[0]
		


session = Session.get_session()

if session is not None: 
	session.update()
	session.output_headers()