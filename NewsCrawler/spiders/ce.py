import scrapy
import requests
import re
from ..items import CeCrawlerItem
from urllib.parse import urljoin


class CeSpider(scrapy.Spider):
    """中国经济网，脱贫攻坚、时政社会、金融证券、产业市场"""
    name = 'ce'
    allowed_domains = ['ce.cn']
    item = CeCrawlerItem()

    def start_requests(self):
        start_urls = ['http://tuopin.ce.cn/news/',
                      'http://www.ce.cn/xwzx/xinwen/jsyw/',
                      'http://finance.ce.cn/rolling/index.shtml',
                      'http://www.ce.cn/cysc/newmain/yc/jsxw/'
                      ]
        for i in start_urls:
            if 'tuopin' in i:
                yield scrapy.Request(i, callback=self.parse_tuopin, dont_filter=True)
            elif 'jsyw' in i:
                yield scrapy.Request(i, callback=self.parse_jsyw, dont_filter=True)
            elif 'finance' in i:
                yield scrapy.Request(i, callback=self.parse_fiance, dont_filter=True)
            elif 'cysc' in i:
                yield scrapy.Request(i, callback=self.parse_cysc, dont_filter=True)

    def parse(self, response):
        item = response.meta.get('item')
        item['content'] = []
        item['img'] = []
        item['source'] = response.xpath('//span[@id="articleSource"]/text()').extract_first()
        item['published'] = response.xpath('//span[@id="articleTime"]/text()').extract_first()
        p_list = response.xpath('//div[@class="TRS_Editor"]/p')
        for p in p_list:
            p_img = p.xpath('./img')
            if p_img:
                img_link = p_img.xpath('./@src').extract_first()
                item['content'].append(img_link)
                img_content = requests.get(img_link).content
                item['img'].append(img_content)
            else:
                text = p.xpath('./text()').extract_first()
                if text:
                    text = text.strip('\u3000')
                    if text:
                        item['content'].append(text)
        yield item

    def parse_tuopin(self, response):

        li_list = response.xpath('//div[@class="list"]/ul/li[not (@class="sp")]')

        for li in li_list:
            self.item['title'] = li.xpath('./a/text()').extract_first()
            if self.item['title']:
                self.item['title_link'] = urljoin(response.url, li.xpath('./a/@href').extract_first())
                published = li.xpath('./span/text()').extract_first()
                if published:
                    self.item['published'] = published.strip('[]')
                if self.item['title_link']:
                    if self.item:
                        yield scrapy.Request(self.item['title_link'], callback=self.parse, meta={'item': self.item})
        base_url = 'http://tuopin.ce.cn/news/index_%s.shtml'
        page_func = response.xpath('//script').re('createPageHTML\(\d+,.*\)')[0]
        page = re.findall('/d+', page_func)
        if page:
            page = page[0]
        for i in range(1, int(page)):
            yield scrapy.Request(base_url % i, callback=self.parse_tuopin)

    def parse_jsyw(self, response):

        li_list = response.xpath('//div[@class="sec_left"]/ul/li')
        for li in li_list:
            self.item['title'] = li.xpath('./span[@class="f1"]/a/text()').extract_first()
            if self.item['title']:
                self.item['title_link'] = urljoin(response.url,
                                                  li.xpath('./span[@class="f1"]/a/@href').extract_first())
                published = li.xpath('./span[@class="f2"]/text()').extract_first()
                if published:
                    self.item['published'] = published
                if self.item['title_link']:
                    if self.item:
                        yield scrapy.Request(self.item['title_link'], callback=self.parse, meta={'item': self.item})
        base_url = 'http://www.ce.cn/xwzx/xinwen/jsyw/index_%s.shtml'
        page_func = response.xpath('//script').re('createPageHTML\(\d+,.*\)')[0]
        page = re.findall('/d+', page_func)
        if page:
            page = page[0]
        for i in range(1, int(page)):
            yield scrapy.Request(base_url % i, callback=self.parse_jsyw)

    def parse_fiance(self, response):

        td_list = response.xpath('//td[@class="font14"]')
        for td in td_list:
            self.item['title'] = td.xpath('./a/text()').extract_first()
            if self.item['title']:
                self.item['title_link'] = urljoin(response.url, td.xpath('./a/@href').extract_first())
                published = td.xpath('./span/text()').extract_first()
                if published:
                    self.item['published'] = published.strip('[]')
                if self.item['title_link']:
                    if self.item:
                        yield scrapy.Request(self.item['title_link'], callback=self.parse, meta={'item': self.item})
        base_url = 'http://finance.ce.cn/rolling/index_%s.shtml'
        page_func = response.xpath('//script').re('createPageHTML\(\d+,.*\)')[0]
        page = re.findall('/d+', page_func)
        if page:
            page = page[0]
        for i in range(1, page):
            yield scrapy.Request(base_url % i, callback=self.parse_fiance)

    def parse_cysc(self, response):

        li_list = response.xpath('//div[@class="content"]/div/ul/li')
        for li in li_list:
            self.item['title'] = li.xpath('./a/text()').extract_first()
            if self.item['title']:
                self.item['title_link'] = urljoin(response.url, li.xpath('./a/@href').extract_first())
                published = li.xpath('./text()').extract_first()
                if published:
                    self.item['published'] = published.strip('[]')
                if self.item['title_link']:
                    if self.item:
                        yield scrapy.Request(self.item['title_link'], callback=self.parse, meta={'item': self.item})
        base_url = 'http://www.ce.cn/cysc/newmain/yc/jsxw/index_%s.shtml'
        page_func = response.xpath('//script').re('createPageHTML\(\d+,.*\)')[0]
        page = re.findall('/d+', page_func)
        if page:
            page = page[0]
        for i in range(1, int(page)):
            yield scrapy.Request(base_url % i, callback=self.parse_cysc)
