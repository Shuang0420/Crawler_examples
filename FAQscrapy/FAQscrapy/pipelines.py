# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re

class FaqscrapyPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'w')
    def process_item(self, item, spider):
        if item['text']:
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.file.write(line)
        return item
