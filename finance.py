# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FinancePySpider(CrawlSpider):
    name = 'finance.py'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['https://finance.yahoo.com/topic/stock-market-news/']

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #i = {}
        yield{
          'Title':response.xpath('//*[@id="Fin-Stream"]/ul/li/div/div/div[2]/h3/a/text()').getall()

        }
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return 
