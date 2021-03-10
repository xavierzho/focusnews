"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/10
"""
import pymongo

from NewsCrawler.settings import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, maxPoolSize=1024)

coll_list = [
    "caijing",
    "ce",
    'eastmoney',
    'hexun',
    'news',
    'newsqq',
    'sina',
    'wangyi'
]
sum_conn = client['news']['summary']

if __name__ == '__main__':
    for i in coll_list:
        conn = client['news'][i]
        for j in conn.find():
            try:
                sum_conn.insert_one(j)
            except Exception as e:
                print(e)
            else:
                conn.delete_one(j)

