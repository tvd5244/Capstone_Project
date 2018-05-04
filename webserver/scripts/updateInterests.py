# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:40:55 2018

@author: Dr. Fast
"""

from pathlib import Path
import os

def updateInterests(user): 
	index = user.ID
	interests = user.interests
	
	f = open('interests.txt', 'w+')
	linefound = False
	data = f.readlines()
	for line in data:
		if(line[:1] == str(index)):
			linefound = True
			line = f.write(index + ' ' + interests + "\n")
	if(linefound == False):
		f.write(str(index) + ' ' + interests + "\n")
	f.close()

	print(open("account_details.html").read()
		.replace("<?name>", user.name or "unknown")
		.replace("<?mail>", user.mail or "unknown")
		.replace("<?campus>", user.campus or "unknown")
		.replace("<?academic_program>", user.academic_program or "unknown")
		.replace("<?about_me>", user.about_me or "")
		.replace("<?interests>", user.interests or "")
		.replace("<?classes>", user.classes or "")
		.replace("<?message>", message))
	

	

def updateInterests1(user): 
	index = user.ID
	interests = user.interests

	try:
		f = open('interests.txt', 'r')
		newf = open('newInterests.txt', 'w+')
		filefound = False
		for line in f:
			if (line[:1] == str(index)):
				newf.write(str(index) + ", " + interests + "\n")
				filefound = True
			else:
				newf.write(line)
		if(filefound == False): 
			newf.write(str(index) + ", " + interests + "\n")
		f.close()
		newf.close()
		os.remove("interests.txt")
		os.rename('newInterests.txt', 'interests.txt')
	except FileNotFoundError:
		f = open('interests.txt', 'w+')
		f.write(str(index) + ", " + interests + "\n")
		f.close()
		
def updateInterests2(index):
	with open('testfile.txt', 'r') as file:
		data = file.readlines()
	
	print(data)

