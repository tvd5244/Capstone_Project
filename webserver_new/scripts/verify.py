
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

	status = "<?mail> has been verified successfully"
	print(open("signup_verify_result.html", "r").read().replace("<?status>", status).replace("<?mail>", user.mail))

except Exception:
	status = "An error occurred while verifying <?mail>. Your verification link may have expired. Please try registering again." 
	print(open("signup_verify_result.html", "r").read().replace("<?mail>", user.mail).replace("<?status>", status))

