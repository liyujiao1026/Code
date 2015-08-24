## Run in terminal:
## python ./Desktop/linked.py liyujiao1026@gmail.com 04683763716


import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def getPeopleLinks(page):
	links=[]
	for link in page.find_all('a'):
		url=link.get('href')
		if url:
			if 'profile/view?id=' in url:
				links.append(url)
	return links

def getJobLinks(page):
    links=[]

    for link in page.find_all('a'):
        url=link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)

    return links

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def ViewBot(browser):
	visited = {}
	pList=[]
	count = 0
	while True:
		time.sleep(random.uniform(3.5,6.9))
		page = BeautifulSoup(browser.page_source)
		people = getPeopleLinks(page)
		if people:
			for person in people:
				ID = getID(person)
				if ID not in visited:
					pList.append(person)
					visited[ID]=1
		if pList:
			person = pList.pop()
			browser.get(person)
			count += 1
		else:
			jobs= getJobLinks(page)
			if jobs:
				job=random.choice(jobs)
				root='http://www.linkedin.com'
				roots='http://www.linkedin.com'
				if root not in job or roots not in job:
					job ='https://www.linkedin.com'
					browser.get(job)
				else:
					print 'i am lost exiting'
					break
		print "[+]"+browser.title+"Visited! \n("\
				+str(count)+"/"+str(len(pList))+") Vistied/Queue"
def Main():
    parser=argparse.ArgumentParser()
    parser.add_argument('email',help='linkedin email')
    parser.add_argument('password',help='linkedin passwd')
    args= parser.parse_args()
    browser=webdriver.Firefox()
    #browser=webdriver.Chrome('/path/to/chromedriver')
    browser.get('https://linkedin.com/uas/login');

    emailElement = browser.find_element_by_id('session_key-login')
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id('session_password-login')
    passElement.send_keys(args.password)
    passElement.submit()
    os.system('clear')
    print '[+] Success! logged in , bot starting!'
    ViewBot(browser)
    browser.close()

Main()