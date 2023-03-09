# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    title = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    community = scrapy.Field()
    link = scrapy.Field()