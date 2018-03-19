import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
import sqlite3


session = Session.get_session()

if session is not None: 

	user = UserAccount.get_account_by_id(session.get_account_id())
	target = fields.getvalue("target")

	if target is not None: 
		user.add_friend(UserAccount.get_account_by_id(int(target)))
		user.commit()

	print("""
<html>
<head>
<title>Users</title>
<style>

table td {
	border: solid black 0.1em;
}

</style>
</head>
<body>
<table>
<tr>
<th>Users</th>
</tr>
"""	)

	for entry in user.recommend("", 10): 
		print("""
<tr>
<td>
<strong>""" + entry.mail + """</strong>
<br/>
<form action = "/scripts/catalog.py" 
	method = "POST">
<input type = "hidden" 
	name = "target"
	value = \"""" + str(entry.ID) + """"/>
<input type = "submit" 
	value = "add"/>
</form>
</td>
</tr>
"""		)

	print("""
</table>
<hr/>
<p>
Visit the <a href = "/scripts/friends.py">friends page</a> to view added contacts.
</p>
</body>
</html>
"""	)

else: 
	print(open("error_must_login.html", "r").read())