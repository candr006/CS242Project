import requests
import re
import os
from bs4 import BeautifulSoup, SoupStrainer

baseSearchURL = "https://www.geniuskitchen.com/recipe/?pn="
baseSiteURL = "https://www.geniuskitchen.com"
#append number from 1-1989 to searchURL to get all search pages
for pageNum in range(100):
	searchPage = requests.get(baseSearchURL + str(pageNum))
	print(searchPage.content)
	bigSoup = BeautifulSoup(searchPage.content, 'html.parser')

	#use soupstrainer to basically create a filter to only look at a tags with link containing /recipes/food/views/  <--all recipe have that path
	pageLinks = SoupStrainer('a', href=re.compile('www.geniuskitchen.com'))
	#make list using above filter
	allLinks = [tag for tag in BeautifulSoup(searchPage.content, 'html.parser', parse_only=pageLinks)]

	file = open("geniuskitchen.txt","w")

	#for every link we just scraped
	for i in allLinks:	#every 5th because each link on search page has 5 duplicates
		#add extension to end of base site URL to get full page URL
		pageName = i
		
		#grab ingredients and recipe and nutrition stuff from each page and write it to file
		page = requests.get(pageName)
	
		#make the soup for each page
		soup = BeautifulSoup(page.content, 'html.parser')
		print(page.content)
		
		#this grabs all li tags with class=ingredient, stores them in list and writes them to file with header
		ingredients = soup.findAll("li", "data-ingredient")
		if ingredients:
			file.write("---------------INGREDIENTS----------------\n")
			for ingred in ingredients:
				file.write(ingred.get_text(strip=True) + "\n")

		
		recipe = soup.findAll("div", "directions-inner container-xs ol li")
		if recipe:
			file.write("\n--------------PREPARATION----------------\n")
			for step in recipe:
				file.write(step.get_text(strip=True) + "\n")

		#parallel lists containing corresponding nutrition labels and data

		nutrition_facts=soup.findAll("div", "recipe-facts")
		if nutrition_facts:
			file.write("\n-------------NUTRITIONAL INFO--------------\n")
			for i in range(len(nutrition_facts)):
				file.write(i.get_text(strip=True) + "\n")



