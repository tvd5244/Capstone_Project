
import cgi

print("Content-Type: text/html\r\n\r\n")

print("""
<html>
<head>
<style>
table, tr, th, td {
    border: 0.1em solid black; 
}
</style>
</head>
<body>
<h1>the "globals" dictionary.</h1>
""")

def explorer(values, ignore = set(), depth = -1):
    if depth == 0:
        return
    
    if type(values) is dict:
        print("""\
<table>
<tr>
<th>KEY</th>
<th>VALUE</th>
</tr>
"""     )
        
        for k, v in values.items(): 
            print("""\
<tr>
<td>""" + k + """</td>
<td>""")
            explorer(v, ignore, depth - 1)
            print("""</td>
</tr>
"""         )

        print("""\
</table>
"""     )
    elif type(values) is cgi.FieldStorage:
        print("""\
<table>
<tr>
<th>KEY</th>
<th>VALUE</th>
</tr>
"""     )
        
        for k in values.keys(): 
            print("""\
<tr>
<td>""" + k + """</td>
<td>""")
            explorer(values.getvalue(k), ignore, depth - 1)
            print("""</td>
</tr>
"""         )

        print("""\
</table>
"""     )
    else:
        print(values)

explorer(globals())

print("""
<h1>the "field storage" dictionary.</h1>
""")

explorer(cgi.FieldStorage())

print("""
</body>
</html>
""")
