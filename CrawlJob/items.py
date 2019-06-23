# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawljobItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()
    salary = scrapy.Field()
    average_salary = scrapy.Field()
    High_salary = scrapy.Field()
    Low_salary = scrapy.Field()
    #
    company_address = scrapy.Field()
    work_experience = scrapy.Field()
    education = scrapy.Field()
    need_numbers = scrapy.Field()
    release_time = scrapy.Field()
    work_language = scrapy.Field()

    company_name = scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_business = scrapy.Field()

    job_detail = scrapy.Field()
    job_catacategory = scrapy.Field()
    company_detail = scrapy.Field()
    url = scrapy.Field()



