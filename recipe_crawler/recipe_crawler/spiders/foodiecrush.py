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
			recipe_content=soup.findAll("p")
			recipe_tags=soup.findAll("a", attrs={"class": "entry-tags"})
			recipe_name=soup.findAll("h2",attrs={"class": "wprm-recipe-name"})
			recipe_summary= soup.findAll("div",attrs={"class": "wprm-recipe-summary"})
			ingredients= soup.findAll("li",attrs={"class": "wprm-recipe-ingredient"})
			instructions= soup.findAll("div",attrs={"class": "wprm-recipe-instruction-text"})

			if recipe_name:
				print("Recipe Content: \n")
				for p in recipe_content:
					print(p.get_text())

				print("Recipe Tags: \n")
				for i in recipe_tags:
					print(i.get_text())

				print("Recipe Name: \n")
				for i in recipe_name:
					print(i.get_text())

				print("Recipe Summary: \n")
				for i in recipe_summary:
					print(i.get_text())

				print("Recipe Ingredients: \n")
				for i in ingredients:
					print(i.get_text())

				print("Recipe instructions: \n")
				for i in instructions:
					print(i.get_text())

				print("*********************************************************")

	#links2= getLinks(link['href'])
	#links=links+links2


