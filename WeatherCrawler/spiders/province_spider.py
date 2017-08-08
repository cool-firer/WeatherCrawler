# coding:  utf8

import scrapy
import json
import constant

class ProvinceSpider(scrapy.Spider):
    '''
        get province
    '''
    name = 'province_spider'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn/province/']

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
                    'province': li.xpath('.//text()').extract_first()
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
                'city': a.xpath('..//text()').extract_first()
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
        '''
        else:
            counties = []
            for a in response.xpath('//div[@class="navbox"]/span/a'):
                counties.append({
                    'url': a.xpath('@href').extract_first(),
                    'county': a.xpath('..//text()').extract_first()
                })
            for c in counties:
                yield scrapy.Request(c['url'], callable=self.parse_weather)
        '''
    def parse_weather(self, response):
        '''
            解析天气数据
        '''
        print response.url


    def parse_direct_weather(self, response, meta):
        self.logger.info('provicince:%s, city:%s', meta['province'], meta['city'])