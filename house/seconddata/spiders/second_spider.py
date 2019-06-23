#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from seconddata.items import SeconddataItem
import logging


class secondspider(CrawlSpider):
    name = "secondhouse"

    allow_domains = ['qd.fang.lianjia.com']
    start_urls = ['https://qd.lianjia.com/ershoufang/']

    itr = 2

    #def __init__(self):
       # logger = logging.getLogger('mycustomlogger')


    def parse(self, response):

        for link in response.xpath("//ul[contains(@class, 'sellListContent')]/li/a/@href").extract():
            yield scrapy.Request(link, callback=self.parse_item)


            # next_url = response.xpath("//div[contains(@class, 'page-box house-lst-page-box')]/a[last()]/@href").extract()
        if self.itr <= 100:
            next_url = "https://qd.lianjia.com/ershoufang/pg" + str(self.itr)
            yield scrapy.Request(next_url, callback=self.parse)
            logging.info(next_url)
            self.itr = self.itr + 1

        #if next_url:
        #    next_url = "https://qd.lianjia.com/ershoufang/pg" + str(self.itr)


    def parse_item(self, response):
        data = SeconddataItem()

        data['name'] = response.css("div.communityName a.info::text").extract()
        data['price'] = response.css("div.price span.total::text").extract()
        data['price_per_area'] = response.css("div.price div.text div.unitPrice span::text").extract()
        data['area'] = response.css("div.houseInfo div.area div.mainInfo::text").extract()
        data['valid_area'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[5]/text()").extract()
        data['buildtime'] = response.css("div.houseInfo div.area div.subInfo::text").extract()
        data['house_type'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[1]/text()").extract()
        data['house_direction'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[7]/text()").extract()
        data['supply_heating'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[11]/text()").extract()
        data['fitment'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[9]/text()").extract()
        data['address'] = response.css("div.areaName span.info a::text").extract()
        data['payandtax'] = response.css("div.price div.text div.tax span::text").extract()
        data['property_year'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[13]/text()").extract()
        data['floor'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[2]/text()").extract()
        data['building_type'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[6]/text()").extract()
        data['building_structure'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[8]/text()").extract()
        data['household_num'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[10]/text()").extract()
        data['elevator'] = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[12]/text()").extract()
        data['sell_time'] = response.xpath("//div[@class = 'transaction']/div[@class = 'content']/ul/li[1]/text()").extract()
        data['latest_trade'] = response.xpath("//div[@class = 'transaction']/div[@class = 'content']/ul/li[3]/text()").extract()
        data['hold_year'] = response.xpath("//div[@class = 'transaction']/div[@class = 'content']/ul/li[5]/text()").extract()
        data['trade_property'] = response.xpath("//div[@class = 'transaction']/div[@class = 'content']/ul/li[2]/text()").extract()
        data['house_used'] = response.xpath("//div[@class = 'transaction']/div[@class = 'content']/ul/li[4]/text()").extract()

        return data

