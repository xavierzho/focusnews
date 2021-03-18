import scrapy
from time import strftime
from demjson import decode
from requests import get
from copy import deepcopy

from NewsCrawler.items import NewsItem
from NewsCrawler.utils.hexun_temp_time import temp_time
from NewsCrawler.utils.validate_published import validate_replace


class HexunSpider(scrapy.Spider):
    """定时刷新"""
    name = 'hexun'
    allowed_domains = ['hexun.com']
    start_url = 'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=100,101,103,125,105,124,162,194,108,122,121,119,107,116,114,115,182,120,169,170,177,180,118,190,200,155,130,117,153,106&date=%(date)s&page=%(page)s&tempTime=%(temp_time)s'
    current_date = strftime("%Y-%m-%d")
    start_urls = [start_url % {'date': current_date, 'page': 1, 'temp_time': int(temp_time)}]

    def parse(self, response):
        """
        解析和讯即时新闻的接口
        :param response:
        :return:
        """
        # 实例化item对象
        item = NewsItem()
        data = decode(response.text)
        news_list = data['list']
        item['content'] = []
        item['images'] = []
        # 请求详情页
        for news in news_list:
            # print(news)
            item['news_id'] = news['id']
            item['nav_name'] = news['columnName']
            # item['published'] = validate_replace(news['time'])
            item['title'] = news['title']
            item['desc'] = news['desc']
            item['link'] = news['titleLink']
            # 详情页需要过滤
            yield scrapy.Request(item['link'], callback=self.parse_detail, meta={'item': deepcopy(item)})
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
        published = response.xpath('//span[@class="pr20"]/text()').extract_first()
        item['published'] = validate_replace(published)
        item['source'] = response.xpath('//div[@class="tip fl"]/a/text()').extract_first()
        item['source_link'] = response.xpath('//div[@class="tip fl"]/a/@href').extract_first()
        context_box = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p')

        for content in context_box:
            if not content.xpath('./img'):
                text = content.xpath('.//text()').extract()
                if text:
                    item['content'].append(''.join(text))
            else:
                img_url = content.xpath('./img/@src').extract_first()
                item['content'].append(img_url)
                b_data = get(img_url).content
                item['images'].append(b_data)
        yield item
