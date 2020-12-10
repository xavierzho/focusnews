# coding=gbk
import scrapy
import re
import time
import json
import requests

from ..items import SinaNewsCrawlerItem


class SinaSpider(scrapy.Spider):
    """新浪7*24小时全球实时财经新闻直播"""
    name = 'sina'
    allowed_domains = ['sina.com.cn']

    base_url = 'http://zhibo.sina.com.cn/api/zhibo/feed?page=%(page)s&page_size=20&zhibo_id=152&tag_id=0&dire=f&dpc=1&pagesize=20&_=%(time_stamp)s'
    start_urls = [base_url % {'page': 1, 'time_stamp': str(time.time()).replace('.', '')[:-4]}]

    def parse(self, response):
        item = SinaNewsCrawlerItem()
        data = json.loads(response.text)
        data_list = data['result']['data']['feed']['list']
        for i in data_list:
            item['news_id'] = i['id']
            original_content = i['rich_text'].strip().replace('\r\n', '')
            pattern = re.match('【(.*?)】', original_content)
            if pattern:
                pattern2 = re.findall('【(.*?)】(.*)', original_content)
                item['content'] = pattern2[0][1].strip()
                item['title'] = pattern2[0][0].strip()
            else:
                item['content'] = i['rich_text'].strip()
                item['title'] = None
            item['source_link'] = i['docurl']
            item['published'] = i['update_time']
            item['nav_name'] = [tag['name'] for tag in i['tag']]
            media = i['multimedia']
            if media:
                item['media'] = [requests.get(url).content for url in media['img_url']]
            else:
                item['media'] = None
            yield item
        page_info = data['result']['data']['feed']['page_info']
        next_page = page_info['nextPage']
        if not page_info['totalPage'] == page_info['page']:
            yield scrapy.Request(
                self.base_url % {'page': next_page, 'time_stamp': str(time.time()).replace('.', '')[:-4]},
                callback=self.parse,
                )
        else:
            print('爬取完成')


