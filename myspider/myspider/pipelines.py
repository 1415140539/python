# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class MyspiderPipeline(object):
    def process_item(self, item, spider):
    	# 使用json的格式写入数据到本地文件
    	# 把爬虫抓到的数据写到数据库或者本地的文件系统中
    	with open("tecent.json","a",encoding="utf-8") as f:
    		text  = json.dumps(dict(item),ensure_ascii = False )+"\n"
    		f.write(text)
    	return item