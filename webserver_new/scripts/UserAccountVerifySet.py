
import sqlite3
import UserAccountSet
import smtplib
from email.mime.text import MIMEText
import secrets


class UserAccount(UserAccountSet.UserAccount): 

	@property
	def awaiting_verify(self): 
		return VerifyEmail.get_verify_email(self) is not None

	def __str__(self): 
		return "UserAccountVerifySet.UserAccount(mail = " + self.mail + ", pwd = " + self.pwd + ", awaiting_verify = " + str(self.awaiting_verify) + ")"

	@classmethod
	def create(cls, mail, pwd):
		self = UserAccountSet.UserAccount.create(mail, pwd)
		VerifyEmail.create(self)

		return self



class VerifyEmail: 
	conn = sqlite3.connect("accounts.db")
	conn.executescript("""
create table if not exists UserAccountVerifySet (
	ID int, 
	secret String unique, 
	foreign key (ID) references UserAccountSet (ROWID), 
	primary key (ID)
)
""")
	conn.commit()
	conn.close()

	def __init__(self): 
		self.conn = sqlite3.connect("accounts.db")
		

	@classmethod
	def get_verify_email(cls, user): 
		self = cls()
		self.ID = user.ROWID
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select 1 
from UserAccountVerifySet 
where ID = ?
"""		, (self.ID, )).fetchone()
		cursor.close()

		if res is None: 
			del self
			return None

		return res
	
	def do_verify(self, secret): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select 1 
from UserAccountVerifySet 
where ID = ? and secret = ?
"""		, (self.ID, secret, )).fetchone()
		cursor.close()

		if res is None: 
			return False
		
		self.conn.execute("""\
delete from UserAccountVerifySet 
where ID = ? and secret = ?
"""		, (self.ID, secret, ))
		return True

	@classmethod
	def create(cls, user): 
		self = cls()
		self.ID = user.ROWID
		self.conn.execute("""
delete from UserAccountVerifySet 
where ROWID = ?
"""	, (user.ROWID, ))
		self.conn.execute("""
insert into UserAcccountVerifySet 
values (?, ?)
"""		, (user.ROWID, secrets.token_urlsafe))
		return self
	

def print_table(): 
	conn = sqlite3.connect("accounts.db")
	cursor = conn.cursor()
	res = cursor.execute("""\
select ROWID 
from UserAccountVerifySet
"""	)

	for row in res: 
		print(str(UserAccount.get_account(row[0])))
	
	cursor.close()
	conn.close()

