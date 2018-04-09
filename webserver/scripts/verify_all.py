import sqlite3

sqlite_file = 'database.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


c.execute('delete from UserAccountVerifySet')
c.execute('select * from UserAccountVerifySet')
print(c.fetchall())

conn.commit()
conn.close()
