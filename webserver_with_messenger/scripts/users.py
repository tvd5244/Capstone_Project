import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import UserAccount
import database
import sqlite3

html_builder.begin_output()

print("""
<html>
<head>
<style>
table, table td, table th, table tr {
	border: 0.1em solid black;
}
</style>
</head>
<body>
""")

print("""
<table>
<tr>
""")


conn = database.create_conn()
cursor = conn.cursor()
res = cursor.execute("""\
pragma table_info(UserAccountSet)
""")

for row in res: 
	print("<th>" + row[1] + "</th>")

cursor.close()

print("""\
<th>done_verify</th>
</tr>
""")

cursor = conn.cursor()
res = cursor.execute("""\
select * 
from UserAccountSet
""")

for row in res: 
	print("<tr>")
	for x in row: 
		print("<td>" + str(x) + "</td>")
	
	_cursor = conn.cursor()
	_res = _cursor.execute("""\
select 1 
from UserAccountVerifySet 
where ID = ?
"""	, (row[0], )).fetchone()

	print("""
<td>""" + str(_res is None) + """</td>
</tr>
"""	)

	_cursor.close()

cursor.close()
conn.close()

print("""
</table>
</body>
</html>
""")
