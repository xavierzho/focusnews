import scrapy
from random import random
from requests import get
from time import time
from re import match
from json import loads

from NewsCrawler.items import NewsItem
from NewsCrawler.utils.call_nav_map import nav_map
from NewsCrawler.utils.validate_published import validate_replace


class EastmoneySpider(scrapy.Spider):
    """东方财富网7X24小时快讯"""
    name = 'eastmoney'
    allowed_domains = ['eastmoney.com']
    base_url = 'https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_%(page)s_.html?r=%(ran_num)s&_=%(time_stamp)s'
    time_stamp = str(time()).replace('.', '')[:-4]
    ran_num = random()
    start_urls = [base_url % {'page': 1, 'ran_num': ran_num, 'time_stamp': time_stamp}]

    def parse(self, response):
        """解析出详情页的url，并实现翻页"""
        item = NewsItem()
        ajax_data = response.text.replace('var ajaxResult=', '')
        data_list = loads(ajax_data)['LivesList']
        for data in data_list:
            item['news_id'] = data['newsid']
            item['title'] = data['title']
            item['link'] = data['url_unique']

            item['nav_name'] = [nav_map[i] for i in data['column'].split(',') if i in nav_map.keys()]
            item['published'] = validate_replace(data['showtime'])
            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'item': item})
        for page in range(2, 21):
            next_url = self.base_url % {'page': 1, 'ran_num': self.ran_num, 'time_stamp': self.time_stamp}
            yield scrapy.Request(next_url)

    def parse_detail(self, response):
        item = response.meta['item']
        item['source'] = response.xpath('//div[@class="source data-source"]/@data-source').extract_first()
        item['desc'] = response.xpath('//div[@class="b-review"]/text()').extract_first().strip()
        item['content'] = []
        item['images'] = []
        p_list = response.xpath('//div[@id="ContentBody"]/p[not(@class)] | //div[@id="ContentBody"]/center')
        for p in p_list:
            if p.xpath('.//img'):
                img_link = p.xpath('.//img/@src').extract_first()
                # https://dfscdn.dfcfw.com/download/D25618177642896768707.jpg
                if match(r"https://dfscdn\.dfcfw\.com/download/.*", img_link):
                    item['content'].append(img_link)
                    img_content = get(img_link).content
                    item['images'].append(img_content)
            else:
                text = ''.join(p.xpath('.//text()').extract()).strip()
                if text:
                    item['content'].append(text)
        yield item
