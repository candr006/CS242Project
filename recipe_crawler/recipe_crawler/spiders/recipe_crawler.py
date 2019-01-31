from bs4 import BeautifulSoup
import urllib2
import re
import requests
import cookielib

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12;rv:50.0) Gecko/20100101 Firefox/50.0'}
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
url="http://www.geniuskitchen.com/recipe"

request = urllib2.Request(url = url, headers=headers)
html_page = opener.open(request).read()
soup = BeautifulSoup(html_page)
links = []

for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
	#if "geniuskitchen" in link.get('href'):
    links.append(link.get('href'))

recipe_facts=[]
ingredients=[]
directions=[]

for link in links:
	response = requests.get(link, headers=headers)
	soup = BeautifulSoup(response.text,"html.parser")
	recipe_facts=soup.findAll("div", attrs={"class": "recipe-facts"})
	ingredients=soup.findAll("div", attrs={"class": "ingredient-list"})
	directions= soup.findAll("div", attrs={"class": "directions-inner container-xs"})

	if recipe_facts:
		print("Recipe Facts:" +str(recipe_facts))
	if ingredients:
		print("Ingredients: "+str(ingredients))
	if directions:
		print("Directions: "+str(directions))

