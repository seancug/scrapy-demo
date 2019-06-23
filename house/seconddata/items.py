# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeconddataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_per_area = scrapy.Field()
    area = scrapy.Field()
    valid_area = scrapy.Field()
    buildtime = scrapy.Field()
    house_type = scrapy.Field()
    house_direction = scrapy.Field()
    supply_heating = scrapy.Field()
    fitment = scrapy.Field()
    address = scrapy.Field()
    payandtax = scrapy.Field()
    property_year = scrapy.Field()
    floor = scrapy.Field()
    building_type = scrapy.Field()
    building_structure = scrapy.Field()
    household_num = scrapy.Field()
    elevator = scrapy.Field()
    sell_time = scrapy.Field()
    latest_trade = scrapy.Field()
    hold_year = scrapy.Field()
    trade_property = scrapy.Field()
    house_used = scrapy.Field()
