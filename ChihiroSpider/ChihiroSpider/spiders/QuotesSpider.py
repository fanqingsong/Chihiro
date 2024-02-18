# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy.http import Request
from urllib import parse
from ..items import QuotesItem, QuotesItemLoader
import re
from typing import Generator, Any
from scrapy_redis.spiders import RedisSpider


class QuotesSpider(RedisSpider):
    name = 'QuotesSpider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']
    # base_url = 'http://quotes.toscrape.com/'

    redis_key = 'QuotesSpider:start_urls'
    # Number of url to fetch from redis on each attempt
    # Update this as needed - this will be 16 by default (like the concurrency default)
    redis_batch_size = 1

    page_num = 1
    crawled = 0

    custom_settings = {
        "JOBDIR": "spider_info/quotes",
    }

    def parse(self, response) -> Generator[Request, Any, None]:
        logging.info(f'----------------- quotesspider parse -------------------')
        #
        # top_tags = response.xpath("//div[@class='main-top']/div[@class='info']/text()").extract()[0]
        total_nums = 10

        quotes_entries = response.xpath("/html/body/div/div[2]/div[1]/div")
        logging.info("---------------- entries ---------------")
        logging.info(quotes_entries)

        for one_entry in quotes_entries:
            logging.info(f'one_entry = {one_entry}')

            quotes_item = QuotesItem()

            quotes_item['url'] = one_entry.xpath("./span[2]/a/@href").get()
            quotes_item['text'] = one_entry.xpath("./span[1]/text()").get()
            quotes_item['author'] = one_entry.xpath("./span[2]/small/text()").get()

            logging.info(" ------ quotes_item -------")
            logging.info(quotes_item)

            yield quotes_item

            self.crawled += 1

        if self.crawled < total_nums:
            logging.info(f'crawled = {self.crawled}')
            self.page_num += 1

            next_page_url = self.start_urls[0] + "/page/{0}/" .format(self.page_num)
            yield Request(url=next_page_url, callback=self.parse)


