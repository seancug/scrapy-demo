# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import MySQLdb
import MySQLdb.cursors
import logging
import datetime as dt
import time
from twisted.enterprise import adbapi
from hashlib import md5


class CrawljobPipeline(object):
    def __init__(self):
        self.file = open('it.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLSCrawljobPipeline(object):
    def __init__(self, dbpool):
        self.start_time = time.time()
        self.update_count = 0
        self.insert_count = 0
        self.failure_count = 0
        self.dbpool = dbpool
        self.dbpool.runInteraction(self.do_create)

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # d.addBoth(lambda _: item)
        return d

    # 建立数据表
    def do_create(self, conn):
        logging.info("begin create tabel")

        conn.execute("""
                create table if not EXISTS Job_info
                (urlmd5id VARCHAR(100) PRIMARY KEY, job_name VARCHAR(200), salary VARCHAR(25), Low_salary FLOAT(6,1),
                High_salary FLOAT(6,1), average_salary FLOAT(6,1), company_address VARCHAR(200),
                work_experience VARCHAR(100), education VARCHAR(100), need_numbers VARCHAR(100),
                release_time DATE, work_language VARCHAR(100), company_name VARCHAR(200),
               company_type VARCHAR(100), company_size VARCHAR(100), company_business VARCHAR(100),
               job_detail TEXT, job_catacategory TEXT, company_detail TEXT, url VARCHAR(200), scrapy_time DATETIME
               )""")

        logging.info("finish create tabel")

    # 将每行更新或写入数据库中
    def do_upinsert(self, conn, item, spider):
        urlmd5id = md5(item['url'].encode("utf8")).hexdigest()
        now = dt.datetime.now().replace(microsecond=0).isoformat(' ')
        year = dt.datetime.now().year
        release_time = str(year) + '-' + item['release_time']
        print("begin insert/update tabel")
        print(item['job_name'])

        logging.info(item['url'])

        conn.execute("""
                        select 1 from Job_info where urlmd5id = %s
                """, (urlmd5id,))
        ret = conn.fetchone()
        try:
            if ret:
                conn.execute("""
                                update Job_info set job_name = %s, salary = %s, Low_salary = %s,
                                High_salary = %s, average_salary = %s, company_address = %s,
                                work_experience = %s, education = %s, need_numbers = %s, release_time = %s,
                                work_language = %s, company_name = %s, company_type = %s, company_size = %s,
                                company_business = %s, job_detail = %s, job_catacategory = %s, company_detail = %s, url = %s
                                , scrapy_time = %s where urlmd5id = %s """,
                             (item['job_name'], item['salary'], item['Low_salary'], item['High_salary'],
                              item['average_salary'], item['company_address'], item['work_experience'],
                              item['education'], item['need_numbers'], release_time, item['work_language'],
                              item['company_name'], item['company_type'], item['company_size'],
                              item['company_business'],
                              item['job_detail'], item['job_catacategory'], item['company_detail'], item['url'],
                              now, urlmd5id))
                self.update_count += 1
                print("updated tabel\n")
            else:
                conn.execute("""
                                insert into Job_info(urlmd5id, job_name, salary, Low_salary,
                                High_salary, average_salary, company_address,
                                work_experience, education, need_numbers, release_time, work_language,
                                company_name, company_type, company_size, company_business,
                                 job_detail, job_catacategory, company_detail, url, scrapy_time)
                                 values(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (urlmd5id, item['job_name'], item['salary'], item['Low_salary'], item['High_salary'],
                                  item['average_salary'], item['company_address'], item['work_experience'],
                                  item['education'], item['need_numbers'], release_time, item['work_language'],
                                  item['company_name'], item['company_type'], item['company_size'],
                                  item['company_business'],
                                  item['job_detail'], item['job_catacategory'], item['company_detail'], item['url'],
                                  now))
                self.insert_count += 1
                print("inserted tabel\n")
        except:
            self.failure_count += 1

    def _handle_error(self, failue, item, spider):
        logging.error(failue)

    def close_spider(self, spider):
        self.end_time = time.time()

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("$$$$$ Time used:\t%.3f min" % ((self.start_time - self.end_time) / 60.0))
        print("----- Update Numbers:\t%d" % (self.update_count))
        print("##### Insert Numbers:\t%d" % (self.insert_count))
        print("&&&&& Failure Numbers:\t%d" % (self.failure_count))
        print("***** Finished Scrapy *********")

        logging.info("$$$$$ Time used:\t%.3f min" % ((self.start_time - self.end_time) / 60.0))
        logging.info("----- Update Numbers:\t%d" % (self.update_count))
        logging.info("##### Insert Numbers:\t%d" % (self.insert_count))
        logging.info("&&&&& Failure Numbers:\t%d" % (self.failure_count))
