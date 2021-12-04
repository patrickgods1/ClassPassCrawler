# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Studios(scrapy.Item):
    Studio = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    ZipCode = scrapy.Field()
    Telephone = scrapy.Field()
    Website = scrapy.Field()
    Instagram = scrapy.Field()
    Facebook = scrapy.Field()
    Twitter = scrapy.Field()
    Tags = scrapy.Field()
    Link = scrapy.Field()
    Rating = scrapy.Field()
    ReviewCount = scrapy.Field()
    Email = scrapy.Field()
