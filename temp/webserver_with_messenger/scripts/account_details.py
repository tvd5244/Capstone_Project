import html_builder
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount
from getAccountInfo import getAccountInfo
from getAccountInfo import getRecommendations
from getAccountInfo import getClassRecommendations
from updateInterests import updateInterests
import logs

def sanitize(_str): 
	return _str.replace("&", "&amp;").replace("<", "&lt").replace(">", "&gt").replace("\"", "&quot;")

html_builder.begin_output()

session = Session.get_session()

if session is not None: 
	user = UserAccount.get_account_by_id(session.get_account_id())
	accountInfo = getAccountInfo(user)
	interests = fields.getvalue("interests")
	about_me = fields.getvalue("about_me")
	classes = fields.getvalue("classes")

	if about_me is not None: 
		user.about_me = about_me

	if interests is not None: 
		user.interests = interests
		user.classification = getRecommendations(user)
		#updateInterests(user)
	
	if classes is not None: 
		user.classes = classes
		user.classClassification = getClassRecommendations(user.classes)

	user.commit()
	message = "Changes have been committed"
	
	print(open("account_details.html").read()
		.replace("<?name>", user.name or "unknown")
		.replace("<?mail>", user.mail or "unknown")
		.replace("<?campus>", user.campus or "unknown")
		.replace("<?academic_program>", user.academic_program or "unknown")
		.replace("<?about_me>", sanitize(user.about_me) or "")
		.replace("<?interests>", sanitize(user.interests) or "")
		.replace("<?classes>", sanitize(user.classes) or "")
		.replace("<?message>", message))

else: 
	print(open("error_must_login.html", "r").read())
		
