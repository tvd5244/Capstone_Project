
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
); 
create table if not exists Friendships (
	ID integer primary key, 
	friend integer
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


	def remove(self): 
		self.conn.execute("""
delete from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, ))


	def add_friend(self, user): 
		self.conn.execute("""
insert into Friendships 
values (?, ?)
"""		, (self.ID, user.ID, ))


	def remove_friend(self, user): 
		self.conn.execute("""
delete from Friendships 
where ID = ?
"""		, (self.ID, ))


	def get_friends(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select friend 
from Friendships 
where ID = ?
"""		, (self.ID, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]

