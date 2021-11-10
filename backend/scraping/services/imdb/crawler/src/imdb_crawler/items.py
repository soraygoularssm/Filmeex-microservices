# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TopsItem(scrapy.Item):
    tops = scrapy.Field()

class MediaItem(scrapy.Item):
    id = scrapy.Field()
    details = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()