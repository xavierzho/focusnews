import scrapy


class NewsItem(scrapy.Item):
    _id = scrapy.Field()  # mongodb主键
    published = scrapy.Field()  # 推送时间
    source = scrapy.Field()  # 来源
    source_link = scrapy.Field()  # 来源链接
    title = scrapy.Field()  # 新闻标题
    link = scrapy.Field()  # 新闻详情链接
    content = scrapy.Field()  # 新闻体
    news_id = scrapy.Field()  # 网站内部的id
    desc = scrapy.Field()  # 描述
    nav_link = scrapy.Field()  # 分类链接
    nav_name = scrapy.Field()  # 分类名
    keywords = scrapy.Field()  # 新闻关键字
    images = scrapy.Field()  # 图片
    editor = scrapy.Field()  # 编辑者
