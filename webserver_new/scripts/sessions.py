
from UserAccountVerifySet import UserAccount

class Sessions: 

	conn = sqlite3.connect("database.db")
	conn.executescript("""
create if not exists Sessions (
	secret Text primary key, 
	acc_id Integer foreign key references (UserAccountSet.ROWID)
)
"""	)
	conn.commit()
	conn.close()

	def __init__(self): 
		self.conn = sqlite3.connect("database.db")


	def __del__(self): 
		self.conn.close()


	@classmethod
	def get_account_by_session(cls, secret): 
		self = cls()
		cursor = self.conn.cursor()
		res = cursor.execute("""
select acc_id 
from Sessions 
where secret = ?
"""		, (secret, )).fetchone()

		if res is None: 
			return None

		user = UserAccount.get_account_by_id(res[0])
		cursor.close()

		if user is None: 
			return None

		self = cls()
		self.user = user
		return self

	
	def commit(self): 
		self.conn.commit()


	@classmethod
	def login(cls, mail, pwd): 
		user = UserAccount.get_account(mail)
		
		if user is None or user.pwd != pwd: 
			return None

		self = cls()
		self.user = user

		return self


	def logout(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
delete from Sessions 
where acc_id = ?
"""		, (self.acc_id, ))


	def get_account(self): 
		return UserAccount.get_account_by_id(self.acc_id)
