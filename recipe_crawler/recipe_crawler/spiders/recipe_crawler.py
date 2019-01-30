from bs4 import BeautifulSoup
import urllib2
import re
 
def getLinks(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []
 
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    	#if 'geniuskitchen' in link.get('href'):
        links.append(link.get('href'))

    recipe_facts=[]
    ingredients=[]
    directions=[]
 
    for link in links:
    	html_page = urllib2.urlopen(link)
    	soup = BeautifulSoup(html_page)
    	for rf in soup.findAll("div", {"class": "recipe-facts"}).getText():
    		recipe_facts.append(rf)
    	for i in soup.findAll("div", {"class": "ingredient-list"}).getText():
    		ingredients.append(i)
    	for d in soup.findAll("div", {"class": "directions-inner"}).getText():
    		directions.append(d)

    	print("Recipe Facts:" +recipe_facts)
    	print("Ingredients: "+ingredients)
    	print("Directions: "+directions)
