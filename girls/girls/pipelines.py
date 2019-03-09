# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import time
import urllib
import os
class GirlsPipeline(object):
    def process_item(self, item, spider):
        time_now = time.time()
        path = "F:/myScrapy/girls/girls/spiders/PIC/"
        filename = path + str(time_now) + ".jpg"
        with open(filename,"wb") as f:
            req = urllib.request.urlopen(item['src'])
            f.write(req.read())
        return item
