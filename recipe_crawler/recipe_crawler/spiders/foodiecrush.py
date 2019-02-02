import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import urlparse
import urllib2
import re
import requests
import cookielib
import httplib

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12;rv:50.0) Gecko/20100101 Firefox/50.0'}
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

def getLinks(url):
	links=[]
	if 'www.foodiecrush' in url:
	    page = requests.get(url)
	    soup = BeautifulSoup(page.text, 'html.parser')
	    links = soup.find_all('a')
	    for link in links:
	    	if link not in links:
	        	links.append(link)
	return links

links = getLinks("https://www.foodiecrush.com/recipes")
for link in links:
	#print(link['href'])
	if 'www.' in link['href']:
		request = urllib2.Request(url = link['href'], headers=headers)
		r=requests.get(link['href'])

		if(r.status_code==200):
			html_page = requests.get(link['href'])
			soup = BeautifulSoup(html_page.text, 'html.parser')
			recipe_facts=soup.findAll("article", attrs={"class": "post"})

			if recipe_facts:
				for fact in recipe_facts:
					print(fact.get_text())
				print("*********************************************************")

	#links2= getLinks(link['href'])
	#links=links+links2


