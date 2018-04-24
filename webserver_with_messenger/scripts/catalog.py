import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

# HTML IN THIS FILE IS COPIED IN recommend_table_entry.html

html_builder.begin_output()

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
<html>
<head>
	<title>Recommendations</title>
	<link href="../css/master.css" type="text/css" rel="stylesheet"/>
</head>

<body class="grey_bg">
	<!--<img class="logo" src="/css/lionpals logo.png"/>-->

	<div class="topnav">
		<a class = "active" href="../home.html">Home</a>
    	<a class = "active" href="/scripts/friends.py">Friends</a>
    	<a class = "active" href="../messenger.html">Messenger</a>
    	<a class = "active" href="/scripts/catalog.py">Recommendations</a>
    	<a class = "active" href="../about.html">About Us</a>
    	<a class = "active" href="../support.html">Support</a>
		<a class = "navbar_right" href="/scripts/logout.py">Logout</a>
		<a class = "navbar_right" href="/scripts/account_details.py">Account</a>
  	</div>

  	<div class="container">

  	<div class="separator">hi</div>
  	<div class="rec_left">
		<div class="rec_table">
			<div class="rec_header">
				Recommendations
			</div>
"""	)

	recommendations = user.recommend("", 10)

	for entry in user.recommend("", 10):
		print("""
			<div class="rec_row">
				<div class="rec_col_left">
					<strong>""" + entry.mail + """</strong>
				</div>

				<div class="rec_col_right">
					<form action = "/scripts/catalog.py"
						method = "POST">
						<input type = "hidden"
							name = "addition"
							value = \"""" + str(entry.ID) + """"/>
						<input class="rec_button"
							type = "submit"
							value = "Send Request"/>
					</form>
				</div>
			</div>
"""		)

	print("""
		</div>
"""	)

	if len(recommendations) == 0:
		print("""
		<p>No recommendations available at this time</p>
"""		)

	print("""
	</div> <!-- ends left column -->

	<div class="separator">hi</div>
	""")

	print("""
	<div class="rec_right">
		<div class="rec_table">
			<div class="rec_header">
				Incoming Requests
			</div>
"""	)

	requests = user.get_friend_requests_pending()

	for entry in requests:
		print("""
			<div class="req_row">
				<div class="rec_col_left">
					<strong>""" + entry.mail + """</strong>
				</div>

				<div class="rec_col_right">

					<form action = "/scripts/catalog.py"
						method = "POST">
						<input type = "hidden"
						name = "addition"
						value = \"""" + str(entry.ID) + """"/>
					<input class="req_button"
						type = "submit"
						value = "Accept"/>

					<form action = "/scripts/catalog.py"
						method = "POST">
						<input type = "hidden"
							name = "rejection"
							value = \"""" + str(entry.ID) + """"/>
						<input class="req_button"
							type = "submit"
							value = "Reject"/>
					</form>
				</div>
			</div>
"""		)

	print("""
		</div>
"""	)

	if len(requests) == 0:
		print("""
		<p>No pending requests at this time</p>
"""		)


	print("""
	</div> <!-- ends right column -->
</div> <!-- ends main container -->
</body>
</html>
"""	)

else:
	print(open("error_must_login.html", "r").read())
