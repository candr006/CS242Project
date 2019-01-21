import scrapy

class RecipeSpider(scrapy.Spider):
	name = 'recipes'

	def start_requests(self):
	    urls = [
	        'https://www.geniuskitchen.com/recipe/',
	    ]
	    for url in urls:
	        yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
	    page = response.url.split("/")[-2]
	    filename = 'out_recipe-%s.html' % page
	    with open(filename, 'wb') as f:
	        f.write(response.body)
	    self.log('Saved file %s' % filename)

