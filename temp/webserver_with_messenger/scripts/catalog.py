import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
from getAccountInfo import getAccountInfo
from getAccountInfo import getRecommendations


session = Session.get_session()

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
<!DOCTYPE html>
<html lang="en">


<head>
<title>Recommendations</title>
<link href="/css/master.css" type="text/css" rel="stylesheet"/>

</head>

<div class="topnav">
    <a class = "active" href="home.html">Home</a>
    <a class = "active" href="friends.html">Friends</a>
    <a class = "active" href="messenger.html">Messenger</a>
    <a class = "active" href="recommendations.html">Recommendations</a>
    <a class = "navbar_right" href="/scripts/logout.py">Logout</a>
    <a class = "navbar_right" href="/scripts/account_details.py">Account</a>
</div>

<body class="grey_bg">
	<!-- <img class="logo" src="/css/lionpals logo.png"/> -->
	<table>
	<tr>
		<th>Recommendations</th>
	</tr>
"""	)

	recommendations = user.recommend("", 10)
	
	#recommendations = getAccountInfo(user.interests)
	

	for entry in user.recommend("", 10): 
		accountInfo = getAccountInfo(entry.mail)
		print("""
<tr>
<td>
<strong>""" + entry.mail + """</strong>
<br/>
		""")
		
		if accountInfo:
			print("""
			<strong>""" + accountInfo[0] + """</strong>
			<br/>
			<strong>""" + accountInfo[3] + """</strong>
			<br/>
			<strong>""" + accountInfo[4] + """</strong>
			<br/>
			""")
		
		print("""
		
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
	
	print("""
<tr>
<td>
<p>""" + getRecommendations() + """</p>

</td>
</tr>
"""		)



else: 
	print(open("error_must_login.html", "r").read())