#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import DropItem

class Home_item(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    where = scrapy.Field()
    address = scrapy.Field()
    sellor = scrapy.Field()
    opentime = scrapy.Field()
    gettime = scrapy.Field()
    alltime = scrapy.Field()
    
class homespider(CrawlSpider):
    name = 'home'

    allow_domains = ['qd.fang.lianjia.com']
    start_urls = []
    for i in range(1,48):
        start_urls.append('http://qd.fang.lianjia.com/loupan/pg' + str(i))
    
    rules = (Rule(SgmlLinkExtractor(allow=('loupan/p_\w+',), restrict_xpaths = "//div[@class = 'con-box']")),
             Rule(SgmlLinkExtractor(allow=('loupan/p_\w+/xiangqing/')), callback = 'parse_item'),)
        
    def parse_item(self, response):
        torrent = Home_item()
        #=======================================================================
       # deny = ('loupan/p_\w+/xiangce.*', 'loupan/p_\w+/dongtai.*', 'loupan/p_\w+/pinglun.*','loupan/p_\w+/huxingtu.*','loupan/p_\w+/tuijian.*','loupan/p_\w+/peitao.*','loupan/p_\w+/%.*','loupan/p_\w+/xiangqing/%.*','loupan/p_\w+/xiangqing/.+')
        # torrent['name'] = response.xpath("//div[@class = 'col-1']/h2/a/text()").extract()  
        # torrent['address'] = response.xpath("//span[@class = 'region']/text()").extract()
        # torrent['price'] = response.xpath("//span[@class = 'num']/text()").extract()
        # torrent['area'] = response.xpath("//div[@class = 'area']/text()").extract()
        # torrent['square'] = response.xpath("//div[@class = 'area']/span/text()").extract()
        #=======================================================================
        
        torrent['name'] = response.css("div.resb-name::text").extract()
        torrent['price'] = response.css("ul.x-box span.label-val span::text").extract()
        torrent['where'] = response.xpath("//div[@class = 'big-left fl']/ul[1]/li/span[@class = 'label-val']/a/text()").extract()
        torrent['address'] = response.xpath("//div[@class = 'big-left fl']/ul[1]/li[5]/span[@class = 'label-val']/text()").extract()
        torrent['sellor'] = response.xpath("//div[@class = 'big-left fl']/ul[1]/li[7]/span[@class = 'label-val']/text()").extract()
        torrent['opentime'] = response.css("span.fq-open span::text").extract()
        torrent['gettime'] = response.css("span.fq-handover span::text").extract()
        torrent['alltime'] = response.xpath("//div[@class = 'big-left fl']/ul[3]/li[8]/span[@class = 'label-val']/text()").extract()
         
      #  torrent['name'] = response.css("a.clear h1::text").extract()
      #  torrent['address'] = response.css("span.region::text").extract()
     #   torrent['price'] = response.css("p.jiage span.junjia::text").extract()
       # torrent['area'] = response.css("div.area::text").extract()
      #  torrent['square'] = response.css("div.area span::text").extract()
        return torrent



