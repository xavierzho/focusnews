import scrapy
import json
import requests
from ..items import NewsItem
from ..utils.validate_published import validate_replace


class NewsqqSpider(scrapy.Spider):
    """腾讯财经"""
    name = 'newsqq'
    allowed_domains = ['new.qq.com']
    base_api = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=finance&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    start_urls = [base_api]

    def parse(self, response):
        item = NewsItem()
        data_list = json.loads(response.text)['data']['list']
        for data in data_list:
            item['news_id'] = data['article_id']
            item['nav_name'] = [data['category_cn'], data['sub_category_cn']]
            item['title'] = data['title']
            item['link'] = data['url']
            item['editor'] = data['media_name']
            item['published'] = validate_replace(data['publish_time'])
            item['images'] = data['img']
            item['keywords'] = [i['tag_word'] for i in data['tags']]
            yield scrapy.Request(item['link'], meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta.get('item')
        item['source'] = response.xpath('//a[@class="author"]/span/text()').extract_first()
        item['source_link'] = response.xpath('//a[@class="author"]/@href').extract_first()
        item['content'] = []
        item['images'] = []
        p_list = response.xpath('//div[@class="content-article"]/p')
        for p in p_list:
            p_img = p.xpath('./img')
            if p_img:
                img_link = 'https:' + p_img.xpath('./@src').extract_first()
                item['content'].append(img_link)
                img_content = requests.get(img_link).content
                item['images'].append(img_content)
            else:
                text = p.xpath('./text()').extract_first()
                if text:
                    item['content'].append(text)
        yield item
