"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/9
"""
import pymongo

from NewsCrawler.settings import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, maxPoolSize=1024)
db = client['news']


def caijing():
    # caijing
    conn = db['caijing']
    conn.update_many({}, {"$rename": {"title_link": "link", "img": "images"}})  # 修改列名


def ce():
    conn = db['ce']
    conn.update_many({}, {"$rename": {"title_link": "link", "img": "images"}})


def eastmoney():
    conn = db['eastmoney']
    conn.update_many({}, {"$rename": {"detail_link": "link", "summary": "desc"}})


def hexun():
    conn = db['hexun']
    conn.update_many({}, {
        "$rename": {"titleLink": "link", "img": "images", "context": "content", "columnName": 'nav_name'}})


def news():
    conn = db['news']
    conn.update_many({}, {"$rename": {"detail_link": "link", "img": "images"}})


def newsqq():
    conn = db['newsqq']
    conn.update_many({}, {"$rename": {"title_link": "link", "img": "images", "category": 'nav_name'}})


def sina():
    conn = db['sina']
    conn.update_many({}, {"$rename": {"source_link": "link", "media": "images"}})


def wangyi():
    conn = db['wangyi']
    conn.update_many({}, {"$rename": {"title_link": "link", "img": "images"}})


if __name__ == '__main__':
    caijing()
    ce()
    eastmoney()
    sina()
    wangyi()
    newsqq()
    news()
    hexun()
