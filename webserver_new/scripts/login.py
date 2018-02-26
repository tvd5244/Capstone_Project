
import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()

print("""\
Content-Type: text/html
\r\n
""")



print(open("login.html", "r").read())

