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


class SuningSpider(Spider):
    name = "Faq_suning"

    def __init__(self):
        self.base_url = "http://help.suning.com"
        self.start_urls = ['http://help.suning.com/faq/list.htm']

    def parse(self, response):
        html = Selector(response)
        page = html.xpath('//div[@class="nav-con"]/dl/dd/a')
        for i in page:
            item = dict()
            item['title'] = i.xpath('text()').extract_first().strip()
            item['url'] = self.base_url + i.xpath('@href').extract_first()
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        item_1 = response.meta['item_1']
        html = Selector(response)
        page = html.xpath('//div[@class="problem-hot xfstyle hide"]/ul/li/a')
        for i in page:
            item = dict()
            item['title'] = item_1['title'].encode('utf8')
            item['question'] = i.xpath('text()').extract_first().strip()
            item['url'] = self.base_url + i.xpath('@href').extract_first()
            #print item
            yield Request(url=item['url'], meta={'item_1': item}, callback=self.third_parse)

    def third_parse(self, response):
        item_1 = response.meta['item_1']
        html = Selector(response)
        page = html.xpath('//div[@id="contentShow"]').extract_first()
        replaceTags = re.compile('<.*?>')
        replaceLine = re.compile('\r|\n|\t')
        page = replaceTags.sub("", page)
        page = re.sub(replaceLine, "", page)
        items=[]
        item = FaqscrapyItem()
        item['title'] = item_1['title'].encode('utf8')
        item['question'] = item_1['question'].encode('utf8')
        item['url'] = item_1['url'].encode('utf8')
        item['text']=page
        print item
        items.append(item)
        return items
