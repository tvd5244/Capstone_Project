import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount


session = Session.get_session()

if session is not None: 

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

	user = UserAccount.get_account_by_id(session.get_account_id())

	for entry in user.find("", 10): 
		print("""
<tr>
<td>""" + entry.email + """</td>
</tr>
"""		)

	print("""
</table>
</body>
</html>
"""	)

else: 
	print(open("error_must_login.html", "r").read())