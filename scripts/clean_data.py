"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/10
"""
import pymongo
import bson
import re
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


def clean_string_space(coll):
    """
    清除字符串类型数据的空格
    :param coll:
    :return:
    """
    conn = client['news'][coll]
    for j in conn.find({"published": {"$ne": None}, "title": {"$ne": None}, "source": {"$exists": True, "$ne": None}},
                       {"_id": 0, "images": 0, "content": 0, "link": 0}):
        published = j['published']
        source = j["source"]
        title = j['title']
        if published:
            conn.update_one(j, {"$set": {"published": published.replace("\r", "").replace('\n', "").strip()}},
                            upsert=True)
        if source:
            conn.update_one(j, {"$set": {"source": source.replace("\r", "").replace('\n', "").strip()}}, upsert=True)
        if title:
            conn.update_one(j, {"$set": {"title": title.replace("\r", "").replace('\n', "").strip()}}, upsert=True)


def published_complete(coll):
    """
    将日期为空的以写入日期填补，不符%Y-%m-%d %H:%M:%S格式的修改
    :param coll:
    :return:
    """
    conn = client["news"][coll]
    for j in conn.find({}, {"images": 0, "content": 0, "link": 0}):
        published = j['published']
        if not published.startswith("2"):
            extra = bson.ObjectId(j['_id']).generation_time
            conn.update_one(j, {"$set": {"published": str(extra)}})
        if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d+", j['published']):
            if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", j["published"]):
                conn.update_one(j, {"$set": {"published": j["published"] + ":00"}})

            elif re.match(r"\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}", j['published']):
                conn.update_one(j, {
                    "$set": {"published": j["published"].replace("年", "-").replace("月", "-").replace("日", "") + ":00"}})


if __name__ == '__main__':
    for i in coll_list:
        print("开启清理:", i)
        clean_string_space(i)
        published_complete(i)
        print(i, ":清理结束")
