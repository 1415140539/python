# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspidertestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #职位名称
    positionName = scrapy.Field()
    #职位连接
    positionLink = scrapy.Field()
    #职位类型
    positionType = scrapy.Field()