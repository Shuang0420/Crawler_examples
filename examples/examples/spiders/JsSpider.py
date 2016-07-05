# -*- coding: utf-8 -*-
import logging
import re
import sys
import scrapy
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://www.jd.com/"
    ]

    def parse(self, response):
        logging.info(u'---------我这个是简单的直接获取京东网首页测试---------')
        guessyou = response.xpath('//div[@id="guessyou"]/div[1]/h2/text()').extract_first()
        logging.info(u"find：%s" % guessyou)
        logging.info(u'---------------success----------------')

class JsSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://www.jd.com/"
    ]

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result, endpoint='render.html',
                                args=splash_args)

    def parse_result(self, response):
        logging.info(u'----------使用splash爬取京东网首页异步加载内容-----------')
        guessyou = response.xpath('//div[@id="guessyou"]/div[1]/h2/text()').extract_first()
        logging.info(u"find：%s" % guessyou)
        logging.info(u'---------------success----------------')
