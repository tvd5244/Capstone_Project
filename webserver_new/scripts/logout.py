
from Session import Session

session = Session.get_session()

if session is not None: 
	session.logout()

print(open("logout.html", "r").read())
