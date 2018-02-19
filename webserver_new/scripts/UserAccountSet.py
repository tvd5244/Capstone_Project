
import sqlite3

class UserAccount: 
	conn = sqlite3.connect("accounts.db")
	conn.executescript("""
create table if not exists UserAccountSet (
	ROWID integer primary key autoincrement, 
	mail String unique, 
	pwd String
)
"""	)
	conn.commit()
	conn.close()
	

	def __init__(self): 
		self.conn = sqlite3.connect("accounts.db")


	def __del__(self): 
		self.conn.close()


	@property
	def mail(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select mail 
from UserAccountSet 
where ROWID == ? 
"""		, (self.ROWID, )).fetchone()[0]
		cursor.close()

		return str(res)


	@mail.setter
	def mail(self, value): 
		self.conn.execute("""\
update UserAccountSet 
set mail = ? 
where ROWID = ?
"""		, (value, self.ROWID, ))


	@property
	def pwd(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select pwd 
from UserAccountSet 
where ROWID == ? 
"""		, (self.ROWID, )).fetchone()[0]
		cursor.close()

		return str(res)


	@pwd.setter
	def pwd(self, value): 
		self.conn.execute("""\
update UserAccountSet 
set pwd = ? 
where ROWID = ?
"""		, (value, self.ROWID, ))


	@classmethod
	def get_account(cls, mail): 
		self = cls()
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select ROWID 
from UserAccountSet 
where mail = ?
"""		, (mail, )).fetchone()
		
		if res is None: 
			del self
			return None

		self.ROWID = res[0]
		cursor.close()
		return self


	@classmethod
	def get_account_by_id(cls, user_id):
		self = cls()
		self.ROWID = user_id
		return self


	def __str__(self): 
		return "UserAccountSet.UserAccount(mail = \"" + str(self.mail) + "\", pwd = \"" + self.pwd + "\")"


	def commit(self): 
		self.conn.commit()


	@classmethod
	def create(cls, mail, pwd): 
		self = cls()
		cursor = self.conn.cursor()
		cursor.execute("""\
insert into UserAccountSet 
(mail, pwd) 
values (?, ?)
"""		, (mail, pwd, ))
		self.ROWID = cursor.lastrowid
		cursor.close()
		return self

	def remove(self): 
		self.conn.execute("""\
delete from UserAccountSet 
where ROWID = ?
"""		, (self.ROWID, ))




def print_table(): 
	conn = sqlite3.connect("accounts.db")

	for row in conn.execute("""\
select * 
from UserAccountSet
"""		): 
		print(row)
	
	conn.close()

