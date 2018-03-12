
import sqlite3
import UserAccountVerifySet


class UserAccount(UserAccountVerifySet.UserAccount): 
	conn = UserAccountVerifySet.UserAccount.conn
	conn.executescript("""
create table if not exists UserAccountPropertySet (
	ID integer primary key, 
	interests Text, 
	program Text, 
	foreign key (ID) references UserAccountSet (ID)
)
""")
	conn.commit()


	def __init__(self, conn, ID):
		super().__init__(conn, ID)
		self.conn.execute("""
insert into UserAccountPropertySet 
select ?, ?, ? 
from UserAccountPropertySet 
where not exists (
select 1 
from UserAccountPropertySet 
where ID = ?
)
"""		, (self.ID, "", "", self.ID, ))



	@property
	def interests(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select interests 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return ""

		return res[0]

	
	@interests.setter
	def interests(self, text): 
		self.conn.execute("""
update UserAccountPropertySet 
set interests = ? 
where ID = ?
"""		, (text, self.ID, ))


	@property
	def program(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select program 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return ""

		return res[0]

	
	@program.setter
	def program(self, text): 
		self.conn.execute("""
update UserAccountPropertySet 
set program = ? 
where ID = ?
"""		, (text, self.ID, ))

