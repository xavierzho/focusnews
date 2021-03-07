import scrapy
import random
import json
import requests
import time
from ..items import CaiJingCrawlerItem


class CaijingSpider(scrapy.Spider):
    """需要定时刷新"""
    name = 'caijing'
    allowed_domains = ['caijing.com.cn']

    def start_requests(self):

        start_urls = f'http://roll.caijing.com.cn/ajax_lists.php?modelid=0&time={random.random()}'
        yield scrapy.Request(start_urls, callback=self.parse,
                              headers={
                                  "Referer": "http://roll.caijing.com.cn/",
                                  "X-Requested-With": " XMLHttpRequest"
                              })

    def parse(self, response):
        """
        抓取标题分类
        :param response:
        :return:
        """
        item = CaiJingCrawlerItem()
        data_list = json.loads(response.text)
        for news in data_list:
            item['news_id'] = news['contentid']
            item['nav_name'] = news['cat']
            item['nav_link'] = news['caturl']
            item['title'] = news['title']
            item['title_link'] = news['url']
            item['published'] = time.strftime('%Y') + '-' + news['published']
            yield scrapy.Request(item['title_link'], meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        item['source'] = response.xpath('//span[contains(text(),"来源")]//text()').extract_first()
        item['content'] = []
        item['img'] = []
        contents = response.xpath('//div[@class="article-content"]/p')

        for content in contents:
            if not content.xpath('./img'):
                text = content.xpath('.//text()').extract_first()

                if text:
                    item['content'].append(text)
            else:
                img_url = content.xpath('./img/@src').extract_first()
                item['content'].append(img_url)
                b_data = requests.get(img_url, verify=False).content
                item['img'].append(b_data)
        print(item)
        yield item
