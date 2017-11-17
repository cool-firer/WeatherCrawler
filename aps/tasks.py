#-*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerProcess
from province_spider import ProvinceSpider
from billiard import Process

from scrapy.utils.log import configure_logging
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s', 'LOG_FILE': 'schedule.log'})

def _crawl(path=None):
     crawl = CrawlerProcess({
         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
     })
     crawl.crawl(ProvinceSpider)
     crawl.start()
     crawl.stop()

def run_crawl(path=None):
    p = Process(target=_crawl, args=['hahahahha'])
    p.start()
    #p.join()


scheduler = BlockingScheduler(daemon=True)
scheduler.add_job(run_crawl, "cron", hour=8, minute=30, timezone='Asia/Shanghai')
scheduler.add_job(run_crawl, "cron", hour=12, minute=30, timezone='Asia/Shanghai')
scheduler.add_job(run_crawl, "cron", hour=18, minute=30, timezone='Asia/Shanghai')

try:
	scheduler.start()
except (KeyboardInterrupt, SystemExit):
	scheduler.shutdown()

