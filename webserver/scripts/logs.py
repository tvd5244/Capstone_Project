

def print_line(string): 
	file = open("log.txt", "a")

	file.write(string + "\n")
	file.close()
