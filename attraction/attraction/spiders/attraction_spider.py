import scrapy

from scrapy.selector import Selector
from attraction.items import AttractionItem
from scrapy_splash import SplashRequest
import re

class AttractionSpider(scrapy.Spider):
	name = "attraction"
	allowed_domains = ["tripadvisor.com.vn"]
	start_urls = [
	"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c47-Hanoi.html",
	# "https://www.tripadvisor.com.vn/Attractions-g293925-Activities-c47-Ho_Chi_Minh_City.html"
	]

	for i in range(30, 91):
		if i % 30 == 0:
			url = "https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c47-oa" + str(i) + "-Hanoi.html"
			start_urls.append(url)

	# for i in range(30, 61):
	# 	if i % 30 == 0:
	# 		url = "https://www.tripadvisor.com.vn/Attractions-g293925-Activities-c47-oa" + str(i) + "-Ho_Chi_Minh_City.html"
	# 		start_urls.append(url)

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, self.parse, meta={
				'splash': {
				'endpoint':'render.html',
				'args': {'wait': 0.5},
				},
				}
			)

	def parse(self, response):
		contents = Selector(response).xpath('//div[@class="listing_title "]')
		img_contents = Selector(response).xpath('//div[@class="photo_booking non_generic"]/a/img/@id').extract()
		lazy_img = Selector(response).xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/script[22]/text()').extract()

		for content in contents:
			item = AttractionItem()
			index = contents.index(content)
			item['name'] = content.xpath('a/text()').extract()[0]
			item['url'] = content.xpath('a/@href').extract()[0]
			item['url'] = "https://www.tripadvisor.com.vn/" + item['url']
			item['img_url'] = ""
			item['city_id'] = 0
			try:
				item['img_id'] = img_contents[index]
			except:
				pass
			yield scrapy.Request(item['url'], self.page_parse, meta={
				'splash': {
				'endpoint': 'render.html',
				'args': {'wait': 0.5},
				},
				'item': item,
				})

	def page_parse(self, response):
		item = response.meta['item']
		item['location'] = ""
		try: 
			locationFetch = Selector(response).xpath('//span[@class="street-address"]/text()').extract()[0]
			item['location'] = item['location'] + locationFetch
		except:
			pass
		try:
			locationFetch = Selector(response).xpath('//span[@class="locality"]/text()').extract()[0]
			item['location'] = item['location'] + " " + locationFetch
		except:
			pass
		try:
			locationFetch = Selector(response).xpath('//span[@class="country-name"]/text()').extract()[0]
			item['location'] = item['location'] + " " + locationFetch
		except:
			pass
		item['location'] = re.sub(' +', ' ', item['location']).strip()

		features = Selector(response).xpath('//div[@class="rating_and_popularity"]/span[@class="header_detail attraction_details"]/div[@class="detail"]/a')
		item['features'] = ""
		features_list = []

		for feature in features:
			index = features.index(feature)
			features_list.append(feature.xpath('text()').extract()[0])
			item['features'] = item['features'] + feature.xpath('text()').extract()[0]
			item['features'] = item['features'] + ", "

		item['features'] = item['features'][:-2]

		yield item
