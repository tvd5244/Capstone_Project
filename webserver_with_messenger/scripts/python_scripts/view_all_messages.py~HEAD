import sqlite3

sqlite_file = 'database.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('select mail from UserAccountSet')
print(c.fetchall())
c.execute('select * from messages')
print(c.fetchall())

conn.commit()
conn.close()
