import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re


#this function assumes emails are 1 to 1

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

print(getAccountInfo('njc5250@psu.edu'))
