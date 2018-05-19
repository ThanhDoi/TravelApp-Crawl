# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    star = scrapy.Field()
    img_url = scrapy.Field()
    features = scrapy.Field()
    feature0 = scrapy.Field()
    feature1 = scrapy.Field()
    feature2 = scrapy.Field()
    feature3 = scrapy.Field()
    feature4 = scrapy.Field()
    feature5 = scrapy.Field()
    feature6 = scrapy.Field()
    feature7 = scrapy.Field()
    feature8 = scrapy.Field()
    feature9 = scrapy.Field()
    feature10 = scrapy.Field()
    feature11 = scrapy.Field()