
import sqlite3
import UserAccountVerifySet
import sys
import secrets
import logs


class UserAccount(UserAccountVerifySet.UserAccount): 
	conn = UserAccountVerifySet.UserAccount.conn
	conn.executescript("""
create table if not exists UserAccountPropertySet (
	ID integer primary key, 
	name Text, 
	interests Text, 
	about_me Text, 
	classes Text, 
	program Text, 
	campus Text,
	classification Text,
	classClassification Text,
	foreign key (ID) references UserAccountSet (ID)
); 
create table if not exists Friendships (
	ID integer, 
	friend integer
);
create table if not exists Conversations (
	ID1 integer, 
	ID2 integer, 
	source Text, 
	foreign key (ID1) references UserAccountSet (ID), 
	foreign key (ID2) references UserAccountSet (ID)
)
""")
	conn.commit()


	def __init__(self, conn, ID):
		super().__init__(conn, ID)
#		self.conn.execute("""
#insert into UserAccountPropertySet 
#select ?, ?, ?, ? 
#from UserAccountPropertySet 
#where not exists (
#select 1 
#from UserAccountPropertySet 
#where ID = ?
#)
#"""		, (self.ID, "", "", "", self.ID, ))
		
		cursor = self.conn.cursor()
		res = cursor.execute("""
select 1 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		if res is None: 
			self.conn.execute("""
insert into UserAccountPropertySet 
values (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""			, (self.ID, "", "", "", "", "", "", "",""))


	@property
	def name(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select name 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return ""

		return res[0]

	
	@name.setter
	def name(self, name): 
		self.conn.execute("""
update UserAccountPropertySet 
set name = ? 
where ID = ?
"""		, (name, self.ID, ))

	@property
	def classClassification(self):
		cursor = self.conn.cursor()
		res = cursor.execute("""
select classClassification
from UserAccountPropertySet
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()
		
		if res is None:
			return ""
		
		return res[0]
		
	@classClassification.setter
	def classClassification(self, text):
		self.conn.execute("""
update UserAccountPropertySet
set classClassification = ?
where ID = ?
"""		,(text, self.ID, ))

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
	def about_me(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select about_me 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return None

		return res[0]
	

	@about_me.setter
	def about_me(self, text): 
		self.conn.execute("""
update UserAccountPropertySet 
set about_me = ? 
where ID = ?
"""		, (text, self.ID, ))


	@property
	def classes(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select classes 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()

		if res is None: 
			return None

		return res[0]
	

	@classes.setter
	def classes(self, text): 
		self.conn.execute("""
update UserAccountPropertySet 
set classes = ? 
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

	@property
	def classification(self):
		cursor = self.conn.cursor()
		res = cursor.execute("""
select classification
from UserAccountPropertySet
where ID = ?
"""		, (self.ID, )).fetchone()

		cursor.close()
		
		if res is None:
			return ""
			
		return res[0]
		
	@classification.setter
	def classification(self, text):
		self.conn.execute("""
update UserAccountPropertySet
set classification = ?
where ID = ?
"""		, (text, self.ID))


	def remove(self): 
		self.conn.execute("""
delete from Conversations 
where ID = ?
"""		, (self.ID, ))
		self.conn.execute("""
delete from Friendships 
where ID = ? or friend = ?
"""		, (self.ID, self.ID, ))
		self.conn.execute("""
delete from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, ))
		super().remove()


	@property
	def campus(self): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select campus 
from UserAccountPropertySet 
where ID = ?
"""		, (self.ID, )).fetchone()

		return res[0]

	
	@campus.setter
	def campus(self, text): 
		self.conn.execute("""
update UserAccountPropertySet 
set campus = ? 
where ID = ?
"""		, (text, self.ID, ))


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
	
	def recommendCampus(self, _str, limit):
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
) and ID in (select ID from UserAccountPropertySet where campus = ?)
limit ?
"""		, (self.ID, self.ID, self.ID, _str, limit, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]
		
	def recommendClassClassification(self, _str, limit):
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
) and ID in (select ID from UserAccountPropertySet where classClassification = ?)
limit ?
"""		, (self.ID, self.ID, self.ID, _str, limit, )).fetchall()
		cursor.close()

		return [self.__class__.get_account_by_id(user[0]) for user in res]
		
	def recommendClassification(self, _str, limit):
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
) and ID in (select ID from UserAccountPropertySet where classification = ?)
limit ?
"""		, (self.ID, self.ID, self.ID, _str, limit, )).fetchall()
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


	def create_conversation_source(self, user): 
		cursor = self.conn.cursor()
		res = cursor.execute("""
select source 
from Conversations 
where (ID1 = ? and ID2 = ?) or (ID2 = ? and ID1 = ?)
"""		, (self.ID, user.ID, self.ID, user.ID, )).fetchone()
		cursor.close()

		if res is not None: 
			return res[0]

		source = secrets.token_urlsafe()
		open(source, "w+").close()

		self.conn.execute("""
insert into Conversations 
values (?, ?, ?)
"""		, (self.ID, user.ID, source, ))

		return source

