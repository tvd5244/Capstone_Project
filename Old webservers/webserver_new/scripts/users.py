
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import UserAccount
import sqlite3

print("""\
Content-Type: text/html
\r\n
""")

print("""
<html>
<head>
<style>
table, table td, table th, table tr {
	border: 0.1em solid black;
}
</style>
</head>
<body style = \"
border: 0.1em solid black; 
max-width: 50em; 
margin: auto;
\">
""")

print("""
<table>
<tr>
""")


conn = sqlite3.connect("database.db")
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
