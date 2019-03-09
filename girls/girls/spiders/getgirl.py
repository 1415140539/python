# -*- coding: utf-8 -*-
import scrapy
from ..items import *

class GetgirlSpider(scrapy.Spider):
    name = 'getgirl'
    allowed_domains = ['2717.com']
    start_urls = ['https://www.2717.com/tag/1756.html']

    def parse(self, response):
        item = GirlsItem()
        hrefs = response.css("div.TagPage li>a::attr(href)").getall()
        hrefs_pic = response.css("ul.w110.oh.Tag_list li>a::attr(href)").getall()
        for href_pic in hrefs_pic:
            yield  response.follow(href_pic,self.get_href)
        for href in hrefs:
            yield response.follow(href,self.parse)

    def get_href(self,response):
        hrefs = response.css("ul.articleV4Page.l li>a::attr(href)").getall()
        for href in hrefs:
            if ".html" in href:
                yield response.follow(href,self.get_pic)
    def get_pic(self,response):
        items = GirlsItem()
        src = response.css("p[align=center] img::attr(src)").get()
        title = response.css("p[align=center] img::attr(alt)").get()
        items['src'] = src
        items['title'] = title
        yield items