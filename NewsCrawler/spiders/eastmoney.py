import scrapy
import random
import time
import json

from ..items import NewsItem
from ..utils.call_nav_map import nav_map


class EastmoneySpider(scrapy.Spider):
    """东方财富网7X24小时快讯"""
    name = 'eastmoney'
    allowed_domains = ['eastmoney.com']
    base_url = 'https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_%(page)s_.html?r=%(ran_num)s&_=%(time_stamp)s'
    time_stamp = str(time.time()).replace('.', '')[:-4]
    ran_num = random.random()
    start_urls = [base_url % {'page': 1, 'ran_num': ran_num, 'time_stamp': time_stamp}]

    def parse(self, response):
        """解析出详情页的url，并实现翻页"""
        item = NewsItem()
        ajax_data = response.text.replace('var ajaxResult=', '')
        data_list = json.loads(ajax_data)['LivesList']
        for data in data_list:
            item['news_id'] = data['newsid']
            item['title'] = data['title']
            item['link'] = data['url_unique']

            item['nav_name'] = [nav_map[i] for i in data['column'].split(',') if i in nav_map.keys()]
            item['published'] = data['showtime']
            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'item': item})
        for page in range(2, 21):
            next_url = self.base_url % {'page': 1, 'ran_num': self.ran_num, 'time_stamp': self.time_stamp}
            yield scrapy.Request(next_url)

    def parse_detail(self, response):
        item = response.meta['item']
        item['source'] = ''.join(response.xpath('//p[@class="em_media"]/text()').extract())
        item['summary'] = response.xpath('//div[@class="b-review"]/text()').extract_first().strip()
        item['content'] = []
        p_list = response.xpath('//div[@id="ContentBody"]/p[not (@class="em_media" or @class="res-edit")]')
        for p in p_list:
            p_one = ''.join(p.xpath('./text()').extract()).strip()
            if p_one:
                item['content'].append(p_one)
        yield item
