import html
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

html.begin_output()
session = Session.get_session()

if session is not None:

	user = UserAccount.get_account_by_id(session.get_account_id())
	target = fields.getvalue("target")

	if target is not None:
		user.remove_friend(UserAccount.get_account_by_id(int(target)))

	cancelation = fields.getvalue("cancelation")

	if cancelation is not None:
		user.remove_friend(UserAccount.get_account_by_id(int(cancelation)))

	user.commit()

	print("""
<html>
<head>
<title>Friends</title>
<link href="/css/signup.css" type="text/css" rel="stylesheet"/>
<style>

table td {
	border: solid black 0.1em;
}

</style>
</head>
<body>
<img class="logo" src="/css/lionpals logo.png"/>
<table>
<tr>
<th>My Friends.</th>
</tr>
"""	)

	friends = user.get_friends()

	for friend in user.get_friends():
		print("""
<tr>
<td>
<strong>""" + friend.mail + """</strong>
<form action = "/scripts/friends.py"
	method = "POST">
<input type = "hidden"
	name = "target"
	value = \"""" + str(friend.ID) + """"/>
<br/>
<input type = "submit"
	value = "remove"/>
</form>
<form action = "/scripts/messenger_interface.py"
	method = "GET">
<input type = "hidden"
	name = "target"
	value = \"""" + str(friend.ID) + """"/>
<input type = "submit"
	value = "message"/>
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
No friends at this time.
</p>
"""		)

	print("<br/>")

	print("""
<table>
<tr>
<th>My Requests.</th>
</tr>
"""	)

	requests = user.get_friend_requests()

	for friend in requests:
		print("""
<tr>
<td>
<strong>""" + friend.mail + """</strong>
<form action = "/scripts/friends.py"
	method = "POST">
<input type = "hidden"
	name = "cancelation"
	value = \"""" + str(friend.ID) + """"/>
<br/>
<input type = "submit"
	value = "cancel"/>
</form>
</td>
</tr>
"""		)

	print("""
</table>
"""	)

	if len(requests) == 0:
		print("""
<p>
Nothing to display.
<br/>
Visit the <a href = "/scripts/catalog.py">catalog</a> to add friends.
</p>
"""		)

	print("""
</body>
</html>
"""	)

else:
	print(open("error_must_login.html", "r").read())
