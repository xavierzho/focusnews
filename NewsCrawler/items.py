import scrapy


class NewsItem(scrapy.Item):
    _id = scrapy.Field()
    published = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    news_id = scrapy.Field()
    desc = scrapy.Field()
    nav_link = scrapy.Field()
    summary = scrapy.Field()
    keywords = scrapy.Field()
