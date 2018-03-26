
import sqlite3

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
	pwd String
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


	@property
	def pwd(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select pwd 
from UserAccountSet 
where ID == ? 
"""		, (self.ID, )).fetchone()
		cursor.close()

		return str(res[0])


	@pwd.setter
	def pwd(self, value): 
		self.conn.execute("""\
update UserAccountSet 
set pwd = ? 
where ID = ?
"""		, (value, self.ID, ))


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
		return "UserAccountSet.UserAccount(mail = \"" + str(self.mail) + "\", pwd = \"" + self.pwd + "\")"


	def commit(self): 
		self.conn.commit()


	@classmethod
	def create(cls, mail, pwd): 
		conn = cls.create_conn()
		cursor = conn.cursor()
		try: 
			cursor.execute("""\
insert into UserAccountSet 
(mail, pwd) 
values (?, ?)
"""			, (mail, pwd, ))
		except sqlite3.IntegrityError: 
			raise ACCOUNT_ALREADY_EXISTS()
		
		
		ID = cursor.lastrowid
		cursor.close()
		
		return cls(conn, ID)


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

