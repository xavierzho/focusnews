import scrapy
import time
import demjson
import requests
from copy import deepcopy
from NewsCrawler.utils.hexun_temp_time import temp_time
from ..items import NewscrawlerItem


class HexunSpider(scrapy.Spider):
    """定时刷新"""
    name = 'hexun'
    allowed_domains = ['hexun.com']
    start_url = 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=100,101,103,125,105,124,162,194,108,122,121,119,107,116,114,115,182,120,169,170,177,180,118,190,200,155,130,117,153,106&date=%(date)s&page=%(page)s&tempTime=%(temp_time)s'
    current_date = time.strftime("%Y-%m-%d")
    start_urls = [start_url % {'date': current_date, 'page': 1, 'temp_time': int(temp_time)}]

    def parse(self, response):
        """
        解析和讯即时新闻的接口
        :param response:
        :return:
        """
        # 实例化item对象
        item = NewscrawlerItem()
        data = demjson.decode(response.text)
        news_list = data['list']
        item['context'] = []
        item['img'] = []
        # 请求详情页
        for news in news_list:
            # print(news)
            item['news_id'] = news['id']
            item['columnName'] = news['columnName']
            item['time'] = news['time']
            item['title'] = news['title']
            item['desc'] = news['desc']
            item['titleLink'] = news['titleLink']
            # 详情页需要过滤
            yield scrapy.Request(item['titleLink'], callback=self.parse_detail, meta={'item': deepcopy(item)})
        page_count = (int(data['sum']) // 30) + 1
        # 翻页请求
        for page in range(2, page_count + 1):
            next_url = self.start_url % {'date': self.current_date, 'page': page, 'temp_time': int(temp_time)}
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        """
        解析详情页数据
        :param response:
        :return:
        """
        item = response.meta['item']

        context_box = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p')

        for content in context_box:
            if not content.xpath('./img'):
                text = content.xpath('.//text()').extract()
                if text:
                    item['context'].append(''.join(text))
            else:
                img_url = content.xpath('./img/@src').extract_first()
                item['context'].append(img_url)
                b_data = requests.get(img_url).content
                item['img'].append(b_data)
        yield item
