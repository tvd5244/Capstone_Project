
has_output = False
headers = "Content-Type: text/html\r\n"


def add_header(header):
	global headers

	if has_output:
		raise "unable to set headers, the headers have already been sent."

	headers = headers + header + "\r\n"


def begin_output():
	if has_output:
		raise "unable to set headers, the headers have already been sent."

	print(headers + "\r\n")
