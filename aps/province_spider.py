# coding:  utf8

import scrapy
import constant as constant
from mongo_db import MongoDB
from billiard import Process
from my_logger import Logger

import time

class ProvinceSpider(scrapy.Spider):
    '''
        get province
    '''
    name = 'province_spider'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn/province/']
    
    def __init__(self):
        file_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '.log'
        #self.logger = logger#logging.getLogger('weather.spider')
        self.log = Logger('province_spider', console=False, file_name=file_name).getLogger()
        self.db = MongoDB(
            auth=True,
            host='localhost',
            user='jc',
            password='jc',
            authSource='admin',
            authMechanism='SCRAM-SHA-1')

        self.db.remove('weather', 'wea', {})
        super(ProvinceSpider, self).__init__()

    def parse(self, response):
        '''
            解析省
        '''
        provinces = []
        for li in response.xpath('//div[@class="sheng_rukou"]/ul/li'):
            name = li.xpath('.//text()').extract_first()
            if name not in constant.PIG_ZONE:
                provinces.append({
                    'url': li.xpath('a/@href').extract_first(),
                    'province': name
                })
        for p in provinces:
            yield scrapy.Request(p['url'], callback=self.parse_city, meta=p)

    def parse_city(self, response):
        '''
            解析市/区
        '''
        # 上级省/直辖市
        province_info = response.meta

        cities = []
        for a in response.xpath('//div[@class="navbox"]/span/a'):
            cities.append({
                'url': response.urljoin(a.xpath('@href').extract_first()),
                'city': a.xpath('.//text()').extract_first()
            })
        # shirt, 广东省的主页样式不一样
        if not cities:
            for a in response.xpath('//div[@class="area_Weather"]/ul/li'):
                cities.append({
                    'url': response.urljoin(a.xpath('./a/@href').extract_first()),
                    'city': a.xpath('./a/text()').extract_first()
                })
        for c in cities:
            yield scrapy.Request(c['url'], callback=self.parse_county, meta={
                'province': province_info['province'],
                'city': c['city']
            })
        
        
    def parse_county(self, response):
        '''
            解析县
        '''
        city_info = response.meta

        # 如果是直辖市, 没有下级县, 直接解析天气数据
        if city_info['province'] in constant.DIRECT_CITY:
            self.parse_direct_weather(response, city_info)
        
        else:
            counties = []
            for a in response.xpath('//div[@class="navbox"]/span/a'):
                counties.append({
                    'url': response.urljoin(a.xpath('@href').extract_first()),
                    'county': a.xpath('.//text()').extract_first()
                })
            for c in counties:
                city_info['county'] = c['county']
                yield scrapy.Request(c['url'], callback=self.parse_county_weather, meta=city_info)
        
    def parse_county_weather(self, response):
        '''
            解析县天气数据
        '''
        meta = response.meta
        self._parse_weather(response, meta)


    def parse_direct_weather(self, response, meta):
        '''
            解析直辖市天气数据
        '''
        #self.log.info('provicince:%s, city:%s', meta['province'], meta['city'])
        self._parse_weather(response, meta)


    def _parse_weather(self, response, meta):
        seven_day_weather = []
        for li in response.xpath('//div[@id="7d"]/ul[@class="t clearfix"]/li'):
            # 相对日期
            h1 = li.xpath('./h1/text()').extract_first()
            # 描述
            desc = li.xpath('./p[@class="wea"]/text()').extract_first()
            # 最高、低温度
            max_tem = li.xpath('./p[@class="tem"]/span/text()').extract_first()
            min_tem = li.xpath('./p[@class="tem"]/i/text()').extract_first()
            # 风向
            wind_direction = li.xpath('.//em/span/@title').extract()
            # 风力 可能会有隐患
            wf = li.xpath('.//i/text()').extract()
            wind_force = wf[-1] if len(wf) >= 2 else 'unkonw'

            seven_day_weather.append({
                'day': h1,
                'desc': desc,
                'max_tem': max_tem,
                'min_tem': min_tem,
                'wind_direction': wind_direction,
                'wind_force': wind_force
            })
        self.log.info("========province:%s=======city:%s========county:%s", meta['province'], meta['city'], meta.get('county', None))

        data = {
            'province': meta['province'],
            'city': meta['city'],
            'county': meta.get('county', None),
            'data': seven_day_weather
        }
        self.db.insert('weather', 'wea', data)


def _crawl(path):
	from scrapy.crawler import CrawlerProcess
	crawl = CrawlerProcess({
          'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
          'LOG_FILE': 'text.log',
          'LOG_LEVEL': 'INFO'
	})
	crawl.crawl(ProvinceSpider)
	crawl.start()
	crawl.stop()
 
def run_crawl(path):
	p = Process(target=_crawl, args=['hahahahha'])
	p.start()
	p.join()

if __name__ == '__main__':
	run_crawl('xxx')	
