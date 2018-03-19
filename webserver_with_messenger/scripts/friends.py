import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
import sys

session = Session.get_session()

if session is not None: 

	user = UserAccount.get_account_by_id(session.get_account_id())
	target = fields.getvalue("target")

	if target is not None: 
		user.remove_friend(UserAccount.get_account_by_id(int(target)))
		user.commit()

	friends = user.get_friends()
	
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

	

	for friend in user.get_friends(): 
		print("""
<tr>
<td>
""" + friend.mail + """
<form action = "/scripts/friends.py" 
	method = "POST">
<input type = "hidden" 
	name = "target" 
	value = \"""" + str(friend.ID) + """"/>
<br/>
<input type = "submit" 
	value = "remove"/>
</form>
</td>
</tr>
"""		)

	print("""
</table>
"""	)

	if len(friends) == 0: 
		print("""
<p>
Nothing to display.
<br/>
Visit the <a href = "/scripts/catalog.py">catalog</a> to add friends.
</p>
"""		)

	print("""
<table>
<tr>
<th>Requests</th>
</tr>
"""	)

	for friend in user.get_friend_requests(): 
		print("""
<tr>
<td>
""" + friend.mail + """
<form action = "/scripts/friends.py" 
	method = "POST">
<input type = "hidden" 
	name = "target" 
	value = \"""" + str(friend.ID) + """"/>
<br/>
<input type = "submit" 
	value = "remove"/>
</form>
</td>
</tr>
"""		)

	print("""
</body>
</html>
"""	)

else: 
	print(open("error_must_login.html", "r").read())