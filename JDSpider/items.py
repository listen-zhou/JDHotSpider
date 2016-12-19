# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JdspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = Field()
    bookName = Field()
    author = Field()
    press = Field()
    bookId = Field()
    price = Field()
    disPrice = Field()
