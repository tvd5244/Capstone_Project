
from Session import Session

session = Session.get_session()

if session is not None: 
	session.logout()
	message = "Logout successful"
	print(open("logout_result.html", "r").read().replace("<?message>", message))
else: 
	message = "An error occurred while logging out"
	print(open("logout_result.html", "r").read().replace("<?message>", message))


