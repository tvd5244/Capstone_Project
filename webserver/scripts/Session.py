
import html_builder
from UserAccountVerifySet import UserAccount
import sqlite3
import secrets
import os
import re
import time
import database
import logs
import disable_auto_update_session

TIMEOUT = 60 * 60 * 2

class Session: 
	conn = database.create_conn()
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
		self.conn = database.create_conn()
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
		secret = secrets.token_urlsafe()
		logs.print_line("Session: " + secret)
		self.conn.execute("""
update Sessions 
set secret = ?, 
time = ?
where ID = ?
"""		, (secret, time.time(), self.ID, ))
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
		logs.print_line("Session Cookie: " + self.secret)
		html_builder.add_header("Set-Cookie: SESSION=" + self.secret)
		self.conn.commit()


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

	
	def __str__(self): 
		return "session(ID = " + str(self.ID) + ")"
		


session = Session.get_session()

if session is not None and not(disable_auto_update_session.disable_auto_update): 
	session.update()
	session.output_headers()