
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from UserAccountVerifySet import VerifyEmail, UserAccount

user_id = fields.getvalue("user_id")
secret = fields.getvalue("secret")

try: 
	if not(VerifyEmail.get_verify_email(UserAccount.get_account(user_id)).do_verify(secret)): 
		raise Exception
	
	print(open("verify_success.html", "r").read().replace("<?mail>", UserAccount.get_account(user_id).mail))
except: 
	print(open("verify_failure.html", "r").read())

