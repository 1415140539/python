# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['ht.tencent.com']
    start_urls = ['http://ht.tencent.com/']

    def parse(self, response):
        pass
