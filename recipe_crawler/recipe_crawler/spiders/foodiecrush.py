import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import urlparse
import urllib2
import re
import requests
import cookielib
import httplib
from random import randint
from time import sleep
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12;rv:50.0) Gecko/20100101 Firefox/50.0'}
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

f = open("foodie_crush_output.txt", "w")
#--------------------------------------------------------------
#This code from scrapehero.com prevents being blocked from crawling

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

proxies = get_proxies()
proxy_pool = cycle(proxies)

#End code from scrapehero.com
#-------------------------------------------------------------
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

for j in range(1,31):
	print("page "+str(j)+" of 31")
	links = getLinks("https://www.foodiecrush.com/category/recipes/page/"+str(j)+"/")

	for link in links:
		#f.write(link['href'])
		if 'www.' in link['href']:
			sleep(randint(1,5))
			request = urllib2.Request(url = link['href'], headers=headers)
			try:
				for k in range(1,11):
					proxy = next(proxy_pool)
					r=requests.get(link['href'],proxies={"http": proxy, "https": proxy})
					r.raise_for_status()
			except requests.exceptions.HTTPError as errh:
				print ("Http Error:",errh)
			except requests.exceptions.ConnectionError as errc:
				print ("Error Connecting:",errc)
			except requests.exceptions.Timeout as errt:
				print ("Timeout Error:",errt)
			except requests.exceptions.RequestException as err:
				print ("OOps: Something Else",err)

			if(r.status_code==200):
				html_page = requests.get(link['href'])
				soup = BeautifulSoup(html_page.text, 'html.parser')
				recipe_content=soup.findAll("p")
				recipe_tags=soup.findAll("a", attrs={"class": "entry-tags"})
				recipe_name=soup.findAll("h2",attrs={"class": "wprm-recipe-name"})
				recipe_summary= soup.findAll("div",attrs={"class": "wprm-recipe-summary"})
				ingredients= soup.findAll("li",attrs={"class": "wprm-recipe-ingredient"})
				instructions= soup.findAll("div",attrs={"class": "wprm-recipe-instruction-text"})

				if recipe_name:
					f.write("Recipe Content: \n")
					for i in recipe_content:
						f.write(i.get_text().encode('utf-8'))

					f.write("Recipe Tags: \n")
					for i in recipe_tags:
						f.write(i.get_text().encode('utf-8'))

					f.write("Recipe Name: \n")
					for i in recipe_name:
						f.write(i.get_text().encode('utf-8'))

					f.write("Recipe Summary: \n")
					for i in recipe_summary:
						f.write(i.get_text().encode('utf-8'))

					f.write("Recipe Ingredients: \n")
					for i in ingredients:
						f.write(i.get_text().encode('utf-8'))

					f.write("Recipe instructions: \n")
					for i in instructions:
						f.write(i.get_text().encode('utf-8'))

					f.write("*********************************************************")

		#links2= getLinks(link['href'])
		#links=links+links2


