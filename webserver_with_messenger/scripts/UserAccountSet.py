
import sqlite3
import hashlib
import random
import sys

class ACCOUNT_ALREADY_EXISTS(BaseException): pass

class UserAccount: 
	
	@classmethod
	def create_conn(cls): 
		return sqlite3.connect("database.db")


	conn = sqlite3.connect("database.db")
	conn.executescript("""
create table if not exists UserAccountSet (
	ID Integer primary key autoincrement, 
	mail String unique, 
	pwd_hash String, 
	pwd_salt Integer
)
"""	)
	conn.commit()


	def __init__(self, conn, ID): 
		self.conn = conn
		self.ID = ID


	def __del__(self): 
		self.conn.close()


	@property
	def mail(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select mail 
from UserAccountSet 
where ID == ? 
"""		, (self.ID, )).fetchone()[0]
		cursor.close()

		return str(res)


	@mail.setter
	def mail(self, value): 
		self.conn.execute("""\
update UserAccountSet 
set mail = ? 
where ID = ?
"""		, (value, self.ID, ))


	def set_password(self, pwd): 
		salt = random.randint(0, sys.maxsize)
		md = hashlib.sha256()
		md.update(str(salt).encode())
		md.update(pwd.encode())
		self.conn.execute("""
update UserAccountSet 
set pwd_hash = ?, pwd_salt = ? 
where ID = ?
"""		, (md.digest(), salt, self.ID, ))


	def check_password(self, pwd): 
		cursor = self.conn.cursor()

		pwd_hash, pwd_salt = cursor.execute("""
select pwd_hash, pwd_salt 
from UserAccountSet 
where ID = ?
"""		, (self.ID, )).fetchone()
		md = hashlib.sha256()

		md.update(str(pwd_salt).encode())
		md.update(pwd.encode())

		return md.digest() == pwd_hash
	

	@classmethod
	def get_account(cls, mail): 
		conn = cls.create_conn()
		cursor = conn.cursor()
		res = cursor.execute("""\
select ID 
from UserAccountSet 
where mail = ?
"""		, (mail, )).fetchone()
		
		cursor.close()

		if res is None: 
			return None

		return cls(conn, res[0])


	@classmethod
	def get_account_by_id(cls, ID):
		return cls(cls.create_conn(), ID)


	def __str__(self): 
		return "UserAccountSet.UserAccount(mail = \"" + str(self.mail) + "\")"


	def commit(self): 
		self.conn.commit()


	@classmethod
	def create(cls, mail, pwd): 
		conn = cls.create_conn()
		cursor = conn.cursor()
		try: 
			cursor.execute("""\
insert into UserAccountSet 
(mail) 
values (?)
"""			, (mail, ))
		except sqlite3.IntegrityError: 
			raise ACCOUNT_ALREADY_EXISTS()
		
		ID = cursor.lastrowid
		cursor.close()

		self = cls(conn, ID)

		self.set_password(pwd)
		
		return self


	def remove(self): 
		self.conn.execute("""\
delete from UserAccountSet 
where ID = ?
"""		, (self.ID, ))

	
	def __eq__(self, other): 
		return isinstance(other, self.__class__) and other.ID == self.ID




def print_table(): 
	conn = sqlite3.connect("accounts.db")

	for row in conn.execute("""\
select * 
from UserAccountSet
"""		): 
		print(row)
	
	conn.close()

