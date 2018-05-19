# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AttractionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    location = scrapy.Field()
    features = scrapy.Field()
    img_id = scrapy.Field()