"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/10
"""
import pymongo

from NewsCrawler.settings import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, maxPoolSize=1024)

conn = client['news']['summary']


def find_duplicate():
    conn.aggregate([
        {'$group': {
            '_id': {'title': "$title", 'published': "$published"},  # 去重字段
            'uniqueIds': {'$addToSet': "$_id"},  # 重复数据的id
            'count': {'$sum': 1}  # 重复次数
        }},
        {'$match': {
            'count': {'$gt': 1}  # 匹配重复次数大于1的数据
        }},
        {'$out': 'result'}  # 输出的表名
    ], allowDiskUse=True)


def del_dup():
    for j in client['news']['result'].find():
        for i in j['uniqueIds'][1:]:
            conn.delete_one({"_id": i})


if __name__ == '__main__':
    del_dup()
