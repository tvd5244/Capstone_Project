
from UserAccountVerifySet import UserAccount
import sqlite3
import secrets
import os
import re

class Session: 

	conn = sqlite3.connect("database.db")
	conn.executescript("""
create table if not exists Sessions (
	ROWID Integer primary key autoincrement, 
	secret Text unique, 
	acc_id Integer,
	foreign key (acc_id) references UserAccountSet (ROWID)
)
"""	)
	conn.commit()
	conn.close()

	def __init__(self): 
		self.conn = sqlite3.connect("database.db")


	def __del__(self): 
		self.conn.close()


	@classmethod
	def get_session(cls): 
		regex = re.compile("SESSION=(\\S+)")
		secret = regex.match(os.environ["HTTP_COOKIE"]).group(1)
		self = cls()
		cursor = self.conn.cursor()
		res = cursor.execute("""
select ROWID 
from Sessions 
where secret = ?
"""		, (secret, )).fetchone()

		if res is None: 
			return None

		self.ROWID = res[0]
		cursor.close()
		return self


	def update(self):
		self.conn.execute("""
update Sessions 
set secret = ? 
where ROWID = ?
"""		, (secrets.token_urlsafe(), self.ROWID, ))
		self.conn.commit()


	@classmethod
	def login(cls, mail, pwd): 
		user = UserAccount.get_account(mail)
		
		if user is None or user.pwd != pwd: 
			return None

		self = cls()

		cursor = self.conn.cursor()
		res = cursor.execute("""
insert into Sessions 
(secret, acc_id) 
values (?, ?)
"""		, (secrets.token_urlsafe(), user.ROWID, )).lastrowid
		self.conn.commit()

		cursor.close()
		self.ROWID = res
		return self
	

	@property
	def secret(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select secret 
from Sessions 
where ROWID = ?
"""		, (self.ROWID, )).fetchone()

		if res is None: 
			return None

		cursor.close()

		return res[0]


	def logout(self): 
		self.conn.execute("""
delete from Sessions 
where ROWID = ?
"""		, (self.ROWID, ))
		self.conn.commit()


	def get_account_id(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select acc_id 
from Sessions 
where ROWID = ?
"""		, (self.ROWID, )).fetchone()

		if res is None: 
			return None

		cursor.close()
		return res[0]
		
