import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount


session = Session.get_session()

print("""\
Content-Type: text/html
\r\n
""")

if session is not None: 

	user = UserAccount.get_account_by_id(session.get_account_id())
	addition = fields.getvalue("addition")

	if addition is not None: 
		user.add_friend(UserAccount.get_account_by_id(int(addition)))

	rejection = fields.getvalue("rejection")

	if rejection is not None: 
		user.remove_friend(UserAccount.get_account_by_id(int(rejection)))

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
<th>Recommendations.</th>
</tr>
"""	)

	recommendations = user.recommend("", 10)

	for entry in user.recommend("", 10): 
		print("""
<tr>
<td>
<strong>""" + entry.mail + """</strong>
<br/>
<form action = "/scripts/catalog.py" 
	method = "POST">
<input type = "hidden" 
	name = "addition"
	value = \"""" + str(entry.ID) + """"/>
<input type = "submit" 
	value = "add"/>
</form>
</td>
</tr>
"""		)

	print("""
</table>
"""	)

	if len(recommendations) == 0: 
		print("""
<p>
There are no recommendations available at this time. Please check back later.
</p>
"""		)

	print("<hr/>")

	print("""
<table>
<tr>
<th>Incomming Requests.</th>
</tr>
"""	)

	requests = user.get_friend_requests_pending()

	for entry in requests: 
		print("""
<tr>
<td>
<strong>""" + entry.mail + """</strong>
<br/>
<form action = "/scripts/catalog.py" 
	method = "POST">
<input type = "hidden" 
	name = "rejection"
	value = \"""" + str(entry.ID) + """"/>
<input type = "submit" 
	value = "reject"/>
</form>
<form action = "/scripts/catalog.py" 
	method = "POST">
<input type = "hidden" 
	name = "addition" 
	value = \"""" + str(entry.ID) + """"/>
<input type = "submit" 
	value = "accept"/>
</td>
</tr>
"""		)

	print("""
</table>
"""	)

	if len(requests) == 0: 
		print("""
<p>
There are no pending requests at this time. Please check back later.
</p>
"""		)


	print("""
<hr/>
<p>
Visit the <a href = "/scripts/friends.py">friends page</a> to view added contacts.
</p>
</body>
</html>
"""	)

else: 
	print(open("error_must_login.html", "r").read())