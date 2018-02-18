import sqlite3

sqlite_file = 'test.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('create table testTable (id integer primary key, username varchar, password varchar)')
c.execute('insert into testTable values (0, "john_david_podesta", "password")')
c.execute('select * from testTable')
print(c.fetchall())

conn.commit()
conn.close()
