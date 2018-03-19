
import sqlite3
import UserAccountVerifySet
import sys


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
	ID integer, 
	friend integer
)
""")
	conn.commit()


	def __init__(self, conn, ID):
		super().__init__(conn, ID)
#		self.conn.execute("""
#insert into UserAccountPropertySet 
#select ?, ?, ? 
#from UserAccountPropertySet 
#where not exists (
#select 1 
#from UserAccountPropertySet 
#where ID = ?
#)
#"""		, (self.ID, "", "", self.ID, ))
		



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
	def academic_program(self): 
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

	
	@academic_program.setter
	def academic_program(self, text): 
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
where (ID = ? and friend = ?) or (friend = ? and ID = ?)
"""		, (self.ID, user.ID, self.ID, user.ID, ))


	def get_friends(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select friend 
from Friendships me
where ID = ? 
and exists (
select 1 
from Friendships 
where ID = me.friend 
and friend = me.ID
)
"""		, (self.ID, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]

	
	def get_friend_requests(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select friend 
from Friendships me
where ID = ? 
and not exists (
select 1 
from Friendships 
where ID = me.friend 
and friend = me.ID
)
"""		, (self.ID, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]

	
	def get_friend_requests_pending(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select ID 
from Friendships fr
where friend = ? 
and not exists (
select 1 
from Friendships 
where ID = ? and friend = fr.ID
)
"""		, (self.ID, self.ID, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]


	def recommend(self, _str, limit): 
		cursor = self.conn.cursor()
		res = self.conn.execute("""
select ID 
from UserAccountSet other
where ID <> ? 
and not exists (
select 1 
from Friendships 
where (ID = ? and friend = other.ID)
or (ID = other.ID and friend = ?)
)
limit ?
"""		, (self.ID, self.ID, self.ID, limit, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]


