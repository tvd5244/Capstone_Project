import cgitb; cgitb.enable()
import cgi; fields = cgi.FieldStorage()
import UserAccountSet
from UserAccountPropertySet import UserAccount

print("""\
Content-Type: text/html
\r\n
""")

recipient = fields.getvalue("recipient")
message = fields.getvalue("message")

if recipient is None or message is None: 
    print(open("messenger_send.html", "r").read().replace("<?recipient>", recipient or "").replace("<?message>", message or ""))
else:
    conn = sqlite3.connect("database.db")
    conn.executescript("""
    create table if not exists messages (
    ID Integer primary key autoincrement, 
    sender String,
    recipient String,
    message String
    )
    """	)
    conn.executescript("""
    insert into messages (sender, recipient, message)
    values (""" + sender """,""" + recipient """,""" + """message)
    """ )
    
