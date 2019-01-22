import scrapy

class RecipeSpider(scrapy.Spider):
	name = 'recipes'
	start_urls = [
        'https://www.geniuskitchen.com/recipe/',
    ]

	def parse(self, response):
		body_tag=response.css("body div.fd-site-wrapper div.gk-tile-content")
		i=1
		for tc in body_tag:
			if i==2:
				print('-----------------------------body_tag '+str(body_tag))
				recipe=tc.css("div.tile-stream div.fd-recipe")
				print('-------------------recipe: '+str(recipe))
				it= recipe.css('div.fd-inner-tile')
				print("------------------it: "+str(it))
				iw=it.css('div.fd-img-wrap')
				print("------------------iw: "+str(iw))
				next_page=iw.css('div.inner-wrapper a::attr(href)')

				print("--------------------------------URL: ")
				print(next_page)
				if next_page is not None:
					print("---------------------------here")
					next_page = response.urljoin(str(next_page))
		        	yield scrapy.Request(str(next_page), callback=self.parse)
		        	#response.url.split("/")[-2]
			    	filename = 'outputrecipe-%s.html'
			    	with open(filename, 'a') as f:
			    		f.write(response.body)
			i+=1


