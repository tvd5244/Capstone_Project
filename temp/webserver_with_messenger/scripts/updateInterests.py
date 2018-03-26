# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:40:55 2018

@author: Dr. Fast
"""

from pathlib import Path
import os

def updateInterests(index, interests):
	f = open('interests.txt', 'w+');
	linefound = False;
	data = f.readlines()
	for line in data:
		if(line[:1] == str(index)):
			linefound = True;
			line = f.write(index + ' ' + interests + "\n")
	if(linefound == False):
		f.write(str(index) + ' ' + interests + "\n")
	f.close()
	

	

def updateInterests1(index, interests):
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

