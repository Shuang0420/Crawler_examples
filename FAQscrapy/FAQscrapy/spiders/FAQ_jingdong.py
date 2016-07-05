# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from FAQscrapy.items import FaqscrapyItem
from scrapy.http import Request
from scrapy.selector import Selector
import re


class JingdongSpider(Spider):
    name = "Faq_jingdong"

    def __init__(self):
        self.base_url = "http:"
        self.start_urls = ['http://help.jd.com/user/issue/list-28.html']

    def parse(self, response):
        html = Selector(response)
        page = html.xpath('//div[@class="subside-in"]/dl/dd/ul/li/a')
        for i in page:
            item = dict()
            item['title'] = i.xpath('text()').extract_first().strip()
            item['url'] = self.base_url + i.xpath('@href').extract_first()
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        item_1 = response.meta['item_1']
        html = Selector(response)
        page = html.xpath('//ul[@class="help_list"]/li/a')
        replaceLine = re.compile('<.*?>|\r|\n|\t')
        for i in page:
            item = dict()
            item['title'] = item_1['title'].encode('utf8')
            ques = i.xpath('text()').extract()[-1].strip()
            item['question'] = replaceLine.sub('', ques)
            item['url'] = self.base_url + i.xpath('@href').extract_first()
            #print item
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.third_parse)

    def third_parse(self, response):
        item_1 = response.meta['item_1']
        html = Selector(response)
        page = html.xpath('//div[@class="contxt"]').extract_first()
        replaceTags = re.compile('<.*?>')
        replaceLine = re.compile('\r|\n|\t')
        page = replaceTags.sub("", page)
        page = re.sub(replaceLine, "", page)
        items=[]
        item = FaqscrapyItem()
        item['title'] = item_1['title'].encode('utf8')
        item['question'] = item_1['question'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        item['text']=''.join(page.split())
        print item
        items.append(item)
        return items
