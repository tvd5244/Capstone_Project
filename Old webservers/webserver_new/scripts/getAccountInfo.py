import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re


#this function assumes psu emails are 1 to 1 (i.e only 1 result in student directory per email)

#takes a psu email as a string and returns -1 if no results are found in student directory,
#or a list containing the account info if a result is found.

def getAccountInfo(email):
    r = requests.post('http://www.work.psu.edu/cgi-bin/ldap/ldap_query.cgi', data={'mail': email})
    data = r.text
    soup = bs(data, 'html.parser')
    if ((soup.find(string=re.compile('[0-9]*\smatch(es)?'))[0][0]) == '0'):
        return -1
    else:
        accountInfo = []
        for item in soup.find_all('td'):
            for string in item.stripped_strings:
                accountInfo.append(repr(string))
        accountInfo = list(OrderedDict.fromkeys(accountInfo))
        return accountInfo


