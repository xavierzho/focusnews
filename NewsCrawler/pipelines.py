import pymongo
from .settings import *
from copy import deepcopy
from itemadapter import ItemAdapter


class NewscrawlerPipeline:
    def __init__(self):
        self.mongo_url = MONGO_URL
        self.mongo_db = MONGO_DB
        self.client = None
        self.db = None

    def process_item(self, item, spider):
        if spider.name == 'hexun':
            conn = self.db['hexun']
            copy_item = deepcopy(item)

            conn.insert_one(dict(copy_item))
        elif spider.name == 'caijing':
            conn = self.db['caijing']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'sina':
            conn = self.db['sina']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'eastmoney':
            conn = self.db['eastmoney']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'wangyi':
            conn = self.db['wangyi']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'news':
            conn = self.db['news']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'newsqq':
            conn = self.db['newsqq']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        elif spider.name == 'ce':
            conn = self.db['ce']
            copy_item = deepcopy(item)
            conn.insert_one(dict(copy_item))
        return item

    # 该方法只会在爬虫启动时被调用的时候调用一次
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    # 该方法只会在爬虫结束被调用的时候调用一次
    def close_spider(self, spider):
        self.client.close()



