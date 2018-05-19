import scrapy

from scrapy.selector import Selector
from trip.items import TripItem
from scrapy_splash import SplashRequest
import re

class TripSpider(scrapy.Spider):
	name = "trip"
	allowed_domains = ["tripadvisor.com.vn"]
	start_urls = [
	"https://www.tripadvisor.com.vn/Hotels-g293925-Ho_Chi_Minh_City-Hotels.html",
	# "https://www.tripadvisor.com.vn/Hotel_Review-g293924-d1728680-Reviews-Conifer_Boutique_Hotel-Hanoi.html",
	# "https://www.tripadvisor.com.vn/Hotels-g293924-Hanoi-Hotels.html",
	]

	set_features = [
	"Nhà hàng",
	"Internet tốc độ miễn phí (WiFi)",
	"Quầy bar/Phòng khách",
	"Dịch vụ phòng",
	"Xe đưa đón đến sân bay",
	"Bao gồm bữa sáng",
	"Dịch vụ giặt khô",
	"Dịch vụ giặt là",
	"Nhân viên hỗ trợ khách",
	"Nhân viên đa ngôn ngữ",
	"Spa",
	"Bể bơi"
	]

	# for i in range(30, 1771):
	# 	if i % 30 == 0:
	# 		url = "https://www.tripadvisor.com.vn/Hotels-g293924-oa" + str(i) + "-Hanoi-Hotels.html"
	# 		start_urls.append(url)

	for i in range(30, 2311):
		if i % 30 == 0:
			url = "https://www.tripadvisor.com.vn/Hotels-g293925-oa" + str(i) + "-Ho_Chi_Minh_City-Hotels.html"
			start_urls.append(url)

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
		contents = Selector(response).xpath('//div[@class="listing_title"]')
		img_contents = Selector(response).xpath('//div[@class="aspect  is-shown-at-tablet"]/div[@class="inner"]').extract()

		for content in contents:
			item = TripItem()
			index = contents.index(content)
			item['title'] = content.xpath('a/text()').extract()[0]
			item['url'] = content.xpath('a/@href').extract()[0]
			item['url'] = "https://www.tripadvisor.com.vn/" + item['url']
			item['city_id'] = 1
			try:
				regexRule = re.compile("\((.*?)\)")
				item['img_url'] = regexRule.findall(img_contents[index])[0]
			except:
				try:
					regexRule = re.compile("\"(.*?)\"")
					item['img_url'] = regexRule.findall(img_contents[index])[1]
				except:
					pass
			yield scrapy.Request(item['url'], self.page_parse, meta={
				'splash': {
				'endpoint': 'render.html',
				'args': {'wait': 0.5},
				},
				'item': item,
				})

	def getSingleAddValue(self, response, text="street-address"):
		xpath = str('//span[@class="detail"]/span[@class="') + str(text) + str('"]/text()')
		try:
			returnValue = Selector(response).xpath(xpath).extract()[0]
		except (IndexError):
			returnValue = ""
		return returnValue

	def getAddress(self, response):
		street_add = self.getSingleAddValue(response, text="street-address")
		extended_add = self.getSingleAddValue(response, text="extended-address")
		locality = self.getSingleAddValue(response, text="locality")
		country_name = self.getSingleAddValue(response, text="country-name")
		returnValue = street_add + " " + extended_add + " " + locality + " " + country_name
		returnValue = re.sub(' +', ' ', returnValue).strip()
		return returnValue

	def getFeaturesList(self, response, text=""):
		xpath = str('//div[@class="') + str(text) + str('"]/div[@class="sub_content"]/div[@class="textitem"]')
		result = []
		try:
				features_path = Selector(response).xpath(xpath)
				for each_feature in features_path:
					result.append(each_feature.xpath('text()').extract()[0])
		except(IndexError):
			pass
		return result

	def page_parse(self, response):
		item = response.meta['item']
		item['location'] = self.getAddress(response)
		features_list = []
		features_list.extend(self.getFeaturesList(response, text="ui_column is-6-mobile is-3-tablet is-3-desktop"))
		features_list.extend(self.getFeaturesList(response, text="ui_column is-6-mobile is-3-tablet is-3-desktop mobextra mobspace"))
		item['features'] = set(features_list)
		for i in range(0, 12):
			feature = "feature" + str(i)
			item[feature] = 0

		contents = Selector(response).xpath('//div[@class="ui_column is-12-mobile is-6-tablet"]')
		for content in contents:
			try:
				if content.xpath('div[@class="sub_title"]/text()').extract()[0] == "Khoảng giá":
					item['price'] = content.xpath('div[@class="sub_content"]/div[@class="textitem"]/text()').extract()[0].split('(')[0].strip().replace("\xa0", "")
			except (IndexError):
				pass
		ratings = Selector(response).xpath('//div[@class="starRating detailListItem"]')

		for rating in ratings:
			match = re.search(r'Khách sạn [0-9] sao', rating.extract())
			if match:
				item['star'] = match.group()
			else:
				pass

		for each_feature in features_list:
			if str("Nhà hàng").lower() in str(each_feature).lower():
				item['feature0'] = 1
			if (str("Internet").lower() in str(each_feature).lower()) or (str("WiFi").lower() in str(each_feature).lower()):
				item['feature1'] = 1
			if (str("Quầy bar").lower() in str(each_feature).lower()) or (str("Phòng khách").lower() in str(each_feature).lower()) or (str("Quầy bar").lower() in str(each_feature).lower()):
				item['feature2'] = 1
			if str("Dịch vụ phòng").lower() in str(each_feature).lower():
				item['feature3'] = 1
			if (str("Xe").lower() in str(each_feature).lower()) and (str("sân bay").lower() in str(each_feature).lower()):
				item['feature4'] = 1
			if str("bữa sáng").lower() in str(each_feature).lower():
				item['feature5'] = 1
			if str("giặt khô").lower() in str(each_feature).lower():
				item['feature6'] = 1
			if str("giặt là").lower() in str(each_feature).lower():
				item['feature7'] = 1
			if str("Nhân viên hỗ trợ khách").lower() in str(each_feature).lower():
				item['feature8'] = 1
			if str("Nhân viên đa ngôn ngữ").lower() in str(each_feature).lower():
				item['feature9'] = 1
			if str("Spa").lower() in str(each_feature).lower():
				item['feature10'] = 1
			if str("Bể bơi").lower() in str(each_feature).lower():
				item['feature11'] = 1

		if len(item['features']) == 0:
			return
		else:
			yield item