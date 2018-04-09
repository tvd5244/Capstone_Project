import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re
from DataAnalysisClassifier import classifier

#this function assumes psu emails are 1 to 1 (i.e only 1 result in student directory per email)

#takes a psu email as a string and returns -1 if no results are found in student directory,
#or a list containing the account info if a result is found.

def getAccountInfo(user):
    r = requests.post('http://www.work.psu.edu/cgi-bin/ldap/ldap_query.cgi', data={'mail': user.mail})
    data = r.text
    soup = bs(data, 'html.parser')
    if ((soup.find(string=re.compile('[0-9]*\smatch(es)?'))[0][0]) == '0' or not re.search(re.compile('[a-z]{3}[0-9]*@psu.edu'), user.mail)):
        return []
    else:
        accountInfo = []
        for item in soup.find_all('td'):
            for string in item.stripped_strings:
                accountInfo.append(repr(string))
        accountInfo = list(OrderedDict.fromkeys(accountInfo))
        return accountInfo


def getRecommendations(user):
	f = open('test.csv', 'w')
	f.write("PersonID,Interests")
	f.write("\n")
	f.write("\n")
	f.write("1, " + user.interests)
	f.close()
	classifier()
	print('\n')
	try:
		f = open('final.csv', 'r')
		data = f.readlines()
		returnValue = data[1].split(',')[1]
	except FileNotFoundError:
		returnValue = ""
	else:
		f.close()
		return returnValue
			
		
	
	
	