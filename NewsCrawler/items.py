
import scrapy


class NewscrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    columnName = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    titleLink = scrapy.Field()
    desc = scrapy.Field()
    context = scrapy.Field()
    img = scrapy.Field()


class CaiJingCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    nav_name = scrapy.Field()
    nav_link = scrapy.Field()
    source = scrapy.Field()
    published = scrapy.Field()
    title = scrapy.Field()
    title_link = scrapy.Field()
    content = scrapy.Field()
    img = scrapy.Field()


class SinaNewsCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    source_link = scrapy.Field()
    published = scrapy.Field()
    nav_name = scrapy.Field()
    media = scrapy.Field()


class EasyMoneyCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    detail_link = scrapy.Field()
    img = scrapy.Field()
    published = scrapy.Field()
    source = scrapy.Field()
    nav_name = scrapy.Field()
    summary = scrapy.Field()


class WangYiNewsCrawlerItem(scrapy.Item):
    published = scrapy.Field()
    title = scrapy.Field()
    title_link = scrapy.Field()
    category = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()


class NewsCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    abstract = scrapy.Field()
    detail_link = scrapy.Field()
    source = scrapy.Field()
    published = scrapy.Field()
    keywords = scrapy.Field()
    img = scrapy.Field()


class NewsQQCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    title_link = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    published = scrapy.Field()
    title_img = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()
    keywords = scrapy.Field()


class CeCrawlerItem(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    title_link = scrapy.Field()
    source = scrapy.Field()
    published = scrapy.Field()
    img = scrapy.Field()
    content = scrapy.Field()
