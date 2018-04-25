import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

# THIS HTML IS COPIED IN friends_table_entry.html

html_builder.begin_output()
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
	<link href="/css/master.css" type="text/css" rel="stylesheet"/>
</head>
<body class="grey_bg">

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
				</br>
				<div class="rec_header">
					My Friends
				</div>
"""	)

	friends = user.get_friends()

	for friend in user.get_friends():
		print("""
				<div class="friends_row>
					<div class="rec_col_left">
						<strong>""" + friend.name + """</strong>
						<strong>""" + friend.mail + """</strong>
						<strong>""" + friend.campus + """</strong>
						<strong>""" + friend.academic_program + """</strong>
					</div>
					
					<div class="friends_col_right">
						<form action = "/scripts/messenger_interface.py"
							method = "GET">
							<input type = "hidden"
							name = "target"
							value = \"""" + str(friend.ID) + """\"/>

							<input class="rec_button"
								type = "submit"
								value = "Message"/>
						</form>

						<form action = "/scripts/friends.py"
							method = "POST">
							<input type = "hidden"
								name = "target"
								value = \"""" + str(friend.ID) + """\"/>
							
							<input class="rec_button"
								type = "submit"
								value = "Remove"/>
						</form>
					</div>
				</div>
"""		)

	print("""
			</div>
"""	)

	if len(friends) == 0:
		print("""
			<p>No friends at this time</p>
"""		)

	print("""
		</div>

		<div class="separator">hi</div>

		<div class="rec_right">
			<div class="rec_table">
				</br>
				<div class="rec_header">
					My Requests
				</div>
"""	)

	requests = user.get_friend_requests()

	for friend in requests:
		print("""
				<div class="req_row">
					<div class="rec_col_left">
						<strong>""" + friend.mail + """</strong>
					</div>

					<div class="rec_col_right">
						<form action = "/scripts/friends.py"
							method = "POST">
							<input type = "hidden"
								name = "cancelation"
								value = \"""" + str(friend.ID) + """"/>

							<input type = "submit"
								value = "Cancel"/>
						</form>
					</div>
				</div>
"""		)

	print("""
			</div>
"""	)

	if len(requests) == 0:
		print("""
			<p>No pending friend requests</p>
"""		)

	print("""
		</div>
	</div>
</body>
</html>
"""	)

else:
	print(open("error_must_login.html", "r").read())
