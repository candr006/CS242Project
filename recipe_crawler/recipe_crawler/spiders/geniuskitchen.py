import requests
from bs4 import BeautifulSoup
import urlparse

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12;rv:50.0) Gecko/20100101 Firefox/50.0'}
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

def recursiveUrl(url, link, depth):
    if depth == 5:
        return url
    else:
        
        page = requests.get()
        print(url + link['href'])
        soup = BeautifulSoup(page.text, 'html.parser')
        newlink = soup.find('a')
        if len(newlink) == 0:
            return link
        else:
            return link, recursiveUrl(url, newlink, depth + 1)

def getLinks(url):
	links=[]
	if 'geniuskitchen' in url:
	    page = requests.get(url)
	    soup = BeautifulSoup(page.text, 'html.parser')
	    links = soup.find_all('a')
	    for link in links:
	    	if link not in links:
	        	links.append(link)
	return links

links = getLinks("https://geniuskitchen.com/recipe?pn=2")
for link in links:
	#print('first forloop: '+link['href'])
	print("---------------------------------------------------------\n")
	links2= getLinks(link['href'])
	print(str(links2))
	links=links+links2

for link in links:
	print('second forloop: '+link['href'])
	print(link['href'])
