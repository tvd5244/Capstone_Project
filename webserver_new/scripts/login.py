
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()

print("""\
Content-Type: text/html
\r\n
""")

print(open("scripts/login.html", "r").read())

