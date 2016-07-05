# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from items import FaqscrapyItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from spiders.FAQ_jingdong import JingdongSpider
from spiders.FAQ_suning import SuningSpider
import re


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    runner.crawl(JingdongSpider)
    runner.crawl(SuningSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    reactor.run()
