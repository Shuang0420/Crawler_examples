# -*- coding: utf-8 -*-
import logging
import re
import sys
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest, HtmlResponse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])


class GithubSpider(Spider):
    name = "Github"
    allowed_domains = ["github.com"]
    start_urls = [
        'https://github.com',
    ]
    '''
    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
        "Referer": "https://github.com/",
    }'''

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [Request("https://github.com/login",
                        meta={'cookiejar': 1}, callback=self.post_login)]

    # FormRequeset
    def post_login(self, response):
        # 先去拿隐藏的表单参数authenticity_token
        authenticity_token = response.xpath(
            '//input[@name="authenticity_token"]/@value').extract_first()
        logging.info('authenticity_token=' + authenticity_token)
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数，如果url跟Request页面的一样就省略掉
        return [FormRequest.from_response(response,
                                          url='https://github.com/session',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          #headers=self.post_headers,  # 注意此处的headers
                                          formdata={
                                              #'utf8': '✓',
                                              'login': 'shuang0420',
                                              'password': '#################',
                                              'authenticity_token': authenticity_token
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, response):
        # 登录之后，开始进入要爬取的页面
        for url in self.start_urls:
            logging.info('letter url=' + url)
            yield Request(url, meta={'cookiejar': response.meta['cookiejar']},callback=self.parse_page)


    def parse_page(self, response):
        """comments 内容"""
        logging.info(u'--------------消息分割线-----------------')
        logging.info(response.url)
        replaceTags = re.compile('<.*?>')
        replaceLine = re.compile('\r|\n|\t')
        message = response.xpath(
            '//div[@class="details"]/div[@class="message markdown-body"]|div[@class="message markdown-body"]/blockquote').extract()
        for m in message:
            m = replaceTags.sub("", m)
            m = replaceLine.sub("", m)
            print m
