import sqlite3
import random
import datetime

class UserAccount:
    __conn = sqlite3.connect("database.db")
    __conn.executescript("""\
create table if not exists UserAccountInfo(
    email Text,
    pwd Text
);

create table if not exists UserAccountSet(
    ID int primary key,
    foreign key(ID) references AccountInfo(ROWID)
);

create table if not exists UserAccountVerificationSet(
    acc_ID int primary key, 
    secret Text, 
    date int, 
    foreign key(acc_ID) references AccountInfo(ROWID)
);
""")

    __conn.commit()

    @classmethod
    def create(cls, email, pwd):
        cur = cls.__conn.cursor()
        cur.execute("""\
insert into UserAccountInfo
values(?, ?)
"""     , (email, pwd))
        cls.__conn.commit()
        __cls = cls()
        __cls.__self = cur.lastrowid
        return __cls


    @classmethod
    def get(cls, email):
        res = cls.__conn.execute("""\
select ROWID
from UserAccountSet, UserAccountInfo
where ID == UserAccountInfo.ROWID
"""     ).fetchone()

        if res is None:
            return None

        __cls = cls()
        __cls.__self = res
        return __cls


    def __eq__(self, other):
        return self.__self == other.__self


    def do_verify(self):
        cls.__conn.execute("""\
insert into UserAccountVerificationSet
values(?, ?, ?)
"""     , (__self, random.random(), datetime.datetime.now()))
        




        










