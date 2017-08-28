#-*- coding: utf-8 -*-

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerProcess
from province_spider import ProvinceSpider
from billiard import Process


def remove(path=None):
    '''
    remove file
    :param path:
    :return:
    '''
    print('hah')
    #TODO
    return True

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
    p.join()


import logging
logging.basicConfig()

scheduler = BlockingScheduler()
scheduler.add_job(run_crawl, "interval", minutes=5)

try:
	scheduler.start()
except (KeyboardInterrupt, SystemExit):
	scheduler.shutdown()

