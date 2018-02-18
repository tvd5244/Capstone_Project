import sqlite3

sqlite_file = 'test.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

conn.commit()
conn.close()
