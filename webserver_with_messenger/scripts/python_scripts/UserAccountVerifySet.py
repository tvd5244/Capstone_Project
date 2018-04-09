
import sqlite3
import UserAccountSet
import smtplib
from email.mime.text import MIMEText
import secrets
import socket

ip_addr = socket.gethostbyname("localhost")

class UserAccount(UserAccountSet.UserAccount): 
	conn = UserAccountSet.UserAccount.conn
	conn.executescript("""
create table if not exists UserAccountVerifySet (
	ID integer primary key, 
	secret String unique, 
	foreign key (ID) references UserAccountSet (ID)
)
""")
	conn.commit()


	@property
	def done_verify(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""\
select 1 
from UserAccountVerifySet 
where ID = ?
"""		, (self.ID, )).fetchone()
		cursor.close()

		return res is None


	def __str__(self): 
		return "UserAccountVerifySet.UserAccount(mail = " + self.mail + ", pwd = " + self.pwd + ", awaiting_verify = " + str(self.done_verify) + ")"


	def send_verify_email(self): 
		secret = secrets.token_urlsafe()
		self.conn.execute("""
delete from UserAccountVerifySet 
where ID = ?
"""		, (self.ID, ))
		self.conn.execute("""
insert into UserAccountVerifySet  
(ID, secret)
values (?, ?)
"""		, (self.ID, secret, ))

		server = smtplib.SMTP("smtp.gmail.com:587")
		server.ehlo()
		server.starttls()
		server.login("psulionpals@gmail.com", "ab12cd34")
		message = MIMEText("""
verify link: http://""" + ip_addr + "/scripts/verify.py?user_id=" + str(self.ID) + "&secret=" + secret + """
"""		, "html")
		server.send_message(message, "psulionpals@gmail.com", self.mail)
		server.quit()


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


	def remove(self): 
		self.conn.execute("""\
delete from UserAccountVerifySet 
where ID = ? 
"""		, (self.ID, ))
		super().remove()






def print_table(): 
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	res = cursor.execute("""\
select ROWID 
from UserAccountVerifySet
"""	)

	for row in res: 
		print(str(UserAccount.get_account(row[0])))
	
	cursor.close()
	conn.close()

