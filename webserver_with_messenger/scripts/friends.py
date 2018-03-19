import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount


session = Session.get_session()

if session is not None: 

	print("""
<html>
<head>
<title>Friends</title>
<style>

table td {
	border: solid black 0.1em;
}

</style>
</head>
<body>
<table>
<tr>
<th>Friends</th>
</tr>
"""	)

	user = UserAccount.get_account_by_id(session.get_account_id())

	for friend in user.get_friends(): 
		print("""
<tr>
<td>
""" + friend.email + """
<form action = "/scripts/remote_friend.py" 
	method = "POST">
<input type = "hidden" 
	name = "target" 
	value = """ + friend.ID + """/>
<br/>
<input type = "submit" 
	value = "remove"/>
</form>
</td>
</tr>
"""		)

	print("""
</table>
</body>
</html>
"""	)

else: 
	print(open("error_must_login.html", "r").read())