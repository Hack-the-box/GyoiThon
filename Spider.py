#!/usr/bin/python
# coding:utf-8
import os
import time
import codecs
import scrapy
from scrapy.http import Request
from util import Utilty


class SimpleSpider(scrapy.Spider):
    name = 'simple_spider'

    def __init__(self, category=None, *args, **kwargs):
        super(SimpleSpider, self).__init__(*args, **kwargs)
        self.start_urls = getattr(self, 'target_url', None)
        self.allowed_domains = [getattr(self, 'allow_domain', None)]
        self.delay_time = float(getattr(self, 'delay', None))
        self.store_path = getattr(self, 'store_path', None)
        self.response_log = getattr(self, 'response_log', None)
        self.custom_settings = {
            'DOWNLOAD_DELAY': self.delay_time,
            'ROBOTSTXT_OBEY': True,
            'FEED_EXPORT_ENCODING': 'utf-8'
        }
        log_file = os.path.join(self.store_path, self.response_log)
        self.fout = codecs.open(log_file, 'w', encoding='utf-8')
        Utilty().print_message('ok', 'Save log: {}'.format(log_file))

    def start_requests(self):
        url = self.start_urls
        yield Request(url, self.parse)

    def parse(self, response):
        self.fout.write(response.body.decode('utf-8'))
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            time.sleep(self.delay_time)
            yield scrapy.Request(full_url, callback=self.parse_item)
        for src in response.css('script::attr(src)'):
            full_url = response.urljoin(src.extract())
            time.sleep(self.delay_time)
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        urls = []
        self.fout.write(response.body.decode('utf-8'))
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            urls.append(full_url)
        for src in response.css('script::attr(src)'):
            full_url = response.urljoin(src.extract())
            urls.append(full_url)
        yield {
            'urls': urls,
        }
