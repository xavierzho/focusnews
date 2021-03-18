import scrapy
from random import random
from json import loads
from requests import get
from NewsCrawler.items import NewsItem
from NewsCrawler.utils.validate_published import validate_replace


class CaijingSpider(scrapy.Spider):
    """需要定时刷新"""
    name = 'caijing'
    allowed_domains = ['caijing.com.cn']

    def start_requests(self):

        start_urls = f'http://roll.caijing.com.cn/ajax_lists.php?modelid=0&time={random()}'
        yield scrapy.Request(start_urls, callback=self.parse,
                             headers={
                                 "Referer": "http://roll.caijing.com.cn/",
                                 # "X-Requested-With": " XMLHttpRequest"
                             })

    def source_handler(self, response) -> str:
        """
        来源解析
        source 的表现形式
        1.来源：xxxx
        2. 本文来源于<a>...</a> or span
        3. .news_frome -- 没有来源前缀
        :param response:
        :return:
        """
        res = ""
        source = response.xpath(
            '//span[@class="source_name"]//text()|'
            '//span[@id="source_baidu"]//text()|'
            '//*[@class="news_frome"]//text()').extract()
        res = res.join([i.strip() for i in source])
        if res:
            return res
        else:
            return ''.join(response.xpath('//span[contains(text(),"来源")]//text()').extract())

    def parse(self, response):
        """
        抓取标题分类
        :param response:
        :return:
        """
        item = NewsItem()
        data_list = loads(response.text)
        for news in data_list:
            item['news_id'] = news['contentid']
            item['nav_name'] = news['cat']
            item['nav_link'] = news['caturl']
            item['title'] = news['title']
            item['link'] = news['url']

            yield scrapy.Request(item['link'], meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        item = response.meta['item']
        published = response.xpath('//span[@class="news_time"]/text()|'
                                   '//span[@id="pubtime_baidu"]/text()').extract_first()
        item['published'] = validate_replace(published)
        item['source'] = self.source_handler(response)
        # parse content and images
        item['content'] = []
        item['images'] = []
        contents = response.xpath('//div[@class="article-content"]/p')

        for content in contents:
            if not content.xpath('./img'):
                text = ''.join(content.xpath('.//text()').extract()).strip()
                if text:
                    item['content'].append(text)
            else:
                img_url = content.xpath('./img/@src').extract_first()
                item['content'].append(img_url)
                b_data = get(img_url, verify=False).content
                item['images'].append(b_data)
        yield item
