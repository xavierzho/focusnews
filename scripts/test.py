"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/10
"""
import pymongo
import re

from NewsCrawler.settings import MONGO_URL
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
client = pymongo.MongoClient(MONGO_URL, maxPoolSize=1024)

for i in coll_list:
    conn = client['news'][i]
    for j in conn.find({}, {"_id": 0, "images": 0, "content": 0, "link": 0}):
        if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d+", j['published']):
            if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", j["published"]):
                print(j["published"])

            elif re.match(r"\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}", j['published']):
                print(j["published"])

