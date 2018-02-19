
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import UserAccount

user_id = fields.getvalue("user_id")
secret = fields.getvalue("secret")

try: 
	user = UserAccount.get_account_by_id(user_id)

	if not(user.do_verify(secret)): 
		raise Exception
	
	user.commit()

	print(open("scripts/verify_successful.html", "r").read().replace("<?mail>", user.mail))

except Exception: 
	print(open("scripts/verify_failure.html", "r").read())

