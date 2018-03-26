import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
from Session import Session
from UserAccountPropertySet import UserAccount

session = Session.get_session()
source = fields.getvalue("source")
data = fields.getvalue("data")

print("""\
Content-Type: text/html
\r\n
""")

if source is not None: 
	message = ""

	if data is not None: 
		file = open(source, "a")
		file.write(data + "\n")
		file.close()
		message = "sent."

	print(open("messenger_submit.html", "r").read()
		.replace("<?source>", source)
		.replace("<?message>", message))

else: 
	print(open("error.html", "r").read())