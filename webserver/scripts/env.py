import html_builder
import cgitb; cgitb.enable()
import os

html_builder.begin_output()

print("""
<html>
<head>
<style>
table, table td, table th, table tr {
	border: 0.1em solid black;
}
</style>
</head>
<body>
""")

print("""
<table>
<tr>
<th>Name</th>
<th>Value</th>
</tr>
""")


for key in os.environ: 
	print("""
<tr>
<td>""" + str(key) + """</td>
<td>""" + str(os.environ[key]) + """</td>
</tr>
"""	)

print("""
</table>
</body>
</html>
""")



