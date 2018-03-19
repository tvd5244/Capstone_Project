
from UserAccountVerifySet import UserAccount
import sqlite3
import secrets
import os
import re

class Session: 
	conn = sqlite3.connect("database.db")
	conn.executescript("""
create table if not exists Sessions (
	ID Integer primary key autoincrement, 
	secret Text unique, 
	acc_id Integer,
	foreign key (acc_id) references UserAccountSet (ID)
)
"""	)
	conn.commit()


	def __init__(self, ID): 
		self.conn = sqlite3.connect("database.db")
		self.ID = ID


	def __del__(self): 
		self.conn.close()


	@classmethod
	def get_session(cls): 
		match = re.compile("SESSION=(\\S+)").match(os.environ["HTTP_COOKIE"])
		
		if match is None: 
			return None

		secret = match.group(1)

		cursor = cls.conn.cursor()
		res = cursor.execute("""
select ID 
from Sessions 
where secret = ?
"""		, (secret, )).fetchone()
		cursor.close()

		if res is None: 
			return None
		
		return cls(res[0])


	def update(self):
		self.conn.execute("""
update Sessions 
set secret = ? 
where ID = ?
"""		, (secrets.token_urlsafe(), self.ID, ))
		self.conn.commit()


	@classmethod
	def login(cls, mail, pwd): 
		user = UserAccount.get_account(mail)
		
		if user is None or user.pwd != pwd: 
			return None

		cursor = cls.conn.cursor()
		res = cursor.execute("""
insert into Sessions 
(secret, acc_id) 
values (?, ?)
"""		, (secrets.token_urlsafe(), user.ID, ))
		cls.conn.commit()
		cursor.close()

		return cls(res.lastrowid)
	

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
		
