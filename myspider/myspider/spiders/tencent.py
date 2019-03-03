# -*- coding: utf-8 -*-
import scrapy
from ..items import MyspiderItem
import re
class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
   # 入口url
    # start_urls = []
    start_urls = ['https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0']
    # for i in range(0,100,10):
    	# start_urls.append('https://hr.tencent.com/position.php?keywords=python&lid=2175&tid=0&start='+str(i))
    def parse(self, response):
        '''
        接受到框架返回的抓取结果
        提取到我们真正想要获取到的信息
        '''
        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):
        	item = MyspiderItem()
        	item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]
        	item['positionLink'] = 'https://hr.tencent.com'+each.xpath('./td[1]/a/@href').extract()[0]
        	item['positionType'] = each.xpath('./td[2]/text()').extract()[0]
        	yield item
        # nextUrl = "position.php?keywords=python&lid=2175&tid=0&start=30#a"
        # yield scrapy.Request(nextUrl,callback =self.parse)
        pattern = re.compile('<a href="(position.php\?keywords=python&lid=0&tid=0&start=[\d]+#a)" id="next">下一页')
        nextUrl = re.findall(pattern,response.body.decode())
        if len(nextUrl) > 0:
        	yield scrapy.Request("https://hr.tencent.com/"+nextUrl[0],callback = self.parse)
        # print(response.body.decode())