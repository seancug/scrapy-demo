# coding=utf-8
import scrapy
import scrapy.spiders as sp
from scrapy.linkextractors import LinkExtractor
from CrawlJob.items import CrawljobItem
import re
import logging

class CrawlJobSpider(sp.CrawlSpider):
    name = "Crawl_Job"

    allow_domains = ['https://jobs.51job.com']
    start_urls = ['https://jobs.51job.com/all/']

    rules = (
        sp.Rule(LinkExtractor(allow=(r'https://jobs.51job.com/all/p\d+'))),
        sp.Rule(LinkExtractor(allow=(r'https://jobs.51job.com/.*/\d+.*',)), callback='parse_Item'),
    )

    def parse_Item(self, response):
        Job_item = CrawljobItem()
        Job_item['url'] = response.url
        Job_item['job_name'] = re.sub(r"\(职位编号.*\)",'',response.css("div.cn h1::attr(title)").extract()[0])

        money = response.css("div.cn strong::text").extract()
        Job_item['salary'] = 0.0
        Job_item['Low_salary'] = 0.0
        Job_item['High_salary'] = 0.0
        Job_item['average_salary'] = 0.0
        factormo = 1.0
        factordate = 1.0

        if money:
            Job_item['salary'] = money
            text = money[0]
            if "千" in text:
                factormo = 1000.0
                text = text.replace("千", "")
            elif "万" in text:
                factormo = 10000.0
                text = text.replace("万", "")
            elif "元" in text:
                factormo = 1.0
                text = text.replace("元", "")

            if "月" in text:
                factordate = 1.0
                text = text.replace("月", "")
            elif "年" in text:
                factordate = 1.0 / 12.0
                text = text.replace("年", "")
            elif "天" in text:
                factordate = 31.0
                text = text.replace("天", "")
            elif "小时" in text:
                factordate = 8.0 * 31.0
                text = text.replace("小时", "")

            text = text.replace("/","")
            mo = text.split('-')

            if len(mo) == 2:
                a = float(mo[0]) * factormo * factordate
                b = float(mo[1]) * factormo * factordate
                Job_item['Low_salary'] = a
                Job_item['High_salary'] = b
                Job_item['average_salary'] = (a + b) / 2.0
            elif len(mo) == 1:
                a = float(mo[0]) * factormo * factordate
                Job_item['Low_salary'] = a
                Job_item['High_salary'] = a
                Job_item['average_salary'] = a

        info = response.css("div.cn p[class='msg ltype']::text").extract()
        numlist = len(info)

        company_address = info[0].replace('\n','').replace('\r','').replace('\t','').replace('\xa0','')
        Job_item['company_address'] = company_address.split("-")[0]

        Job_item['work_experience'] = info[1].replace('\xa0', '')

        Job_item['work_language'] = ''

        if numlist == 5:
            Job_item['education'] = info[2].replace('\xa0', '')
            Job_item['need_numbers'] = info[3].replace('\xa0', '')
            Job_item['release_time'] = info[4].replace('\xa0', '').replace('\t', '').replace("发布", '')
            Job_item['work_language'] = '普通话精通'
        elif numlist ==6 or numlist == 7:
            Job_item['education'] = info[2].replace('\xa0', '')
            Job_item['need_numbers'] = info[3].replace('\xa0', '')
            Job_item['release_time'] = info[4].replace('\xa0', '').replace('\t', '').replace("发布", '')
            Job_item['work_language'] = info[5].replace('\xa0', '').replace('\t', '')
        elif numlist == 4:
            Job_item['education'] = 'None'
            Job_item['need_numbers'] = info[2].replace('\xa0', '')
            Job_item['release_time'] = info[3].replace('\xa0', '').replace('\t','').replace("发布", '')
            Job_item['work_language'] = '普通话精通'
        else:
            print(numlist)

        company_name = response.css("div.com_msg > a > p::text").extract()
        if company_name is not None:
            Job_item['company_name'] = company_name

        company_type = response.css("div:nth-child(1) > div.com_tag > p:nth-child(1)::text").extract()
        company_size = response.css("div:nth-child(1) > div.com_tag > p:nth-child(2)::text").extract()
        company_business = response.css("div:nth-child(1) > div.com_tag > p:nth-child(3)::attr(title)").extract()
        if company_type:
            Job_item['company_type'] = company_type
        else:
            Job_item['company_type'] = "None"

        if company_size:
            Job_item['company_size'] = company_size
        else:
            Job_item['company_size'] = "None"

        if company_business:
            Job_item['company_business'] = company_business
        else:
            Job_item['company_business'] = "None"

        job_detail = response.css("div.tCompany_main > div:nth-child(1)").\
             xpath("string(div)").extract()[0].replace('\t','').replace('\n','').replace('\r',' ')

        if job_detail:
            Job_item['job_detail'] = job_detail
        else:
            Job_item['job_detail'] = "None"


        job_catacategory =  response.css("div.tCompany_main > div:nth-child(1) > div > div.mt10").xpath("string(p)").extract()[0].\
             replace('\t','').replace('\n','').replace("职能类别：","").replace("\r"," ")

        if job_catacategory:
            Job_item['job_catacategory'] = job_catacategory
        else:
            Job_item['job_catacategory'] = "None"

        company_detail = response.css("div.tCompany_main > div:last-child").xpath("string(div)").extract()[0].replace('\t','').replace('\n','')
        if company_detail:
            Job_item['company_detail'] = company_detail
        else:
            Job_item['company_detail'] = "None"

        return Job_item
