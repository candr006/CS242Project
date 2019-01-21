import scrapy

class RecipeSpider(scrapy.Spider):
	name = 'recipes'
	start_urls = [
        'https://www.geniuskitchen.com/recipe/',
    ]

	def parse(self, response):
		for recipe in response.css('div.fd-recipe'):
			next_page= recipe.css('div.fd-inner-tile div.fd-img-wrap div.inner-wrapper a::attr(href)').extract_first()
			print("--------------------------------URL: "+next_page)
			if next_page is not None:
				print("---------------------------here")
				next_page = response.urljoin(str(next_page))
	        	yield scrapy.Request(str(next_page), callback=self.parse)
	        	#response.url.split("/")[-2]
		    	filename = 'outputrecipe-%s.html' % page
		    	with open(filename, 'a') as f:
		    		f.write(response.body)


