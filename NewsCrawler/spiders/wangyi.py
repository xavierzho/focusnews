# coding=utf8
import scrapy
import demjson
import requests
from NewsCrawler.settings import *
from ..items import NewsItem
from ..utils.validate_published import validate_replace
"""
详情页url规则：
https://money.163.com/20/1207/23/FT9GGE5900259FVR.html
https://money.163.com/年份/日期/时间（24小时制）/文章ID
"""


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['http://money.163.com/special/00251G8F/news_json.js?%s' % random.random()]
    category_map = {0: '产经', 1: '宏观', 2: '股票', 3: '商业', 4: '基金', 5: '理财', 6: '金融'}

    def parse(self, response):
        item = NewsItem()
        json_str = response.text.replace('var data=', '').strip()[:-1]
        data = demjson.decode(json_str)
        category_list = data['news']
        for category in category_list:
            for news in category:
                item['nav_name'] = self.category_map[news['c']]
                item['link'] = news['l']
                item['title'] = news['t']
                item['published'] = validate_replace(news['p'])
                yield scrapy.Request(item['link'], meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        item['content'] = []
        item['images'] = []
        p_list = response.xpath('//div[@class="post_text"]/p')
        item['title'] = response.xpath('//h1/text()').extract_first()
        source_link = response.xpath('//div[@class="post_info"]/a[not(@class="post_jubao")]')
        if source_link:
            item['source'] = source_link.xpath('./text()').extract_first()
            item['source_link'] = source_link.xpath('./@href').extract_first()
        else:
            source = response.xpath('//div[@class="post_info"]/text()').extract_first()
            if source:
                item['source'] = source.strip().split(' ')[-1]
        for p in p_list:
            p_img = p.xpath('./img')
            if p_img:
                img_link = p_img.xpath('./@src').extract_first()
                item['content'].append(img_link)
                img_content = requests.get(img_link).content
                item['images'].append(img_content)
            else:
                text = p.xpath('./text()').extract_first()
                if text:
                    item['content'].append(text.strip().replace('\n', '').replace('\r', ''))
        if not item['content']:
            p_list = response.xpath('//div[@class="post_body"]/p')
            for p in p_list:
                p_img = p.xpath('./img')
                if p_img:
                    img_link = p_img.xpath('./@src').extract_first()
                    img_content = requests.get(img_link).content
                    item['images'].append(img_content)
                    item['content'].append(img_link)
                else:
                    text = ''.join(p.xpath('.//text()').extract()).strip()
                    if text:
                        item['content'].append(text.replace('\n', '').replace('\r', ''))
        yield item
