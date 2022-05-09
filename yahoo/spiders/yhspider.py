import scrapy
import sys
import datetime
import csv
import dateparser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import HtmlXPathSelector
from yahoo.items import YahooItem


#reload(sys)
#sys.setdefaultencoding('utf-8')
print("Examples of Stocks Symbols are : AAPL, TSLA, NFLX, CAT")
symbol=input("Enter Symbol of Stock : ")

# Load command line parameters
init_url = f"https://finance.yahoo.com/quote/{symbol}/news?p={symbol}"
nextpage_pattern = '//*[@id="render-target-default"]/div/div[3]'
block_pattern = '//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div'
title_pattern = '//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/h3/a/text()'

date_pattern = '//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li/div/div/div[2]/div/span[2]/text()'

FILE_NAME = 'AAPL'


class YhSpider(CrawlSpider):
    name = "yh"  # Unique, name of the spider
    allowed_domains = [
        'finance.yahoo.com'
    ]  # The scraper may move out of yahoo.com through hyperlinks
    # Need to restrict the scraper within yahoo.com domain
    start_urls = [init_url]
    # download_delay = 5 # Uncomment this line if the program stops immediately
    rules = (Rule(LinkExtractor(allow=(),
                                    restrict_xpaths=(nextpage_pattern, )),
                  callback="parse_items",
                  follow=True), )

    def parse_items(self, response):
        items = []
        sel = scrapy.Selector(response)
        sites = sel.xpath(block_pattern)
        for site in sites:
            item = YahooItem()
            item['title'] = site.xpath(title_pattern).get() 
            item['dates']= site.xpath(date_pattern).get()
            
            items.append(item)
            yield item
            

        with open('../dataset' + FILE_NAME + '.csv', 'w+') as f:
            writer = csv.writer(f)
            today = datetime.datetime.now()
            titles=[]
            for item in items:
                # Title processing
                title = ""
                for phrase in item['title']:
                    title += phrase
                title = title.replace('\xc2\xa0', ' ')
                # Date processing
                date_list = item['date'].split(' ')
                date = ""
                day = today.day
                month = today.month
                year = today.year
                if date_list[1] in ['month', 'year', 'months', 'years']:
                    continue
                elif date_list[1] in [
                        'hour', 'hours', 'minute', 'minutes', 'second',
                        'seconds'
                ]:
                    if day < 10:
                        day = '0' + str(day)
                    if month < 10:
                        month = '0' + str(month)
                    date = (year+month+day)
                else:
                    N = int(date_list[0])
                    date_N_days_ago = today - datetime.timedelta(days=N)
                    year = date_N_days_ago.year
                    month = date_N_days_ago.month
                    day = date_N_days_ago.day
                    if day < 10:
                        day = '0' + str(day)
                    if month < 10:
                        month = '0' + str(month)

                    date = (year+month+day)
                   
                date=item['date']
                titles.append(title)
                
                writer.writerows([date, title])
        #print(titles)
        yield items
        return
