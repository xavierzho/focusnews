"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/9
"""
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017", maxPoolSize=1024)
conn = client["news"]["wangyi"]


def fetch_all_sort_published():
    cur = conn.find(no_cursor_timeout=True).sort([
        ("published", -1),
    ])
    with cur:
        for i in cur:
            print(i["title"], i["published"])


fetch_all_sort_published()
