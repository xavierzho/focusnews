"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/10
@Application: 作用在mongodb去重
"""
import pymongo

from NewsCrawler.settings import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, maxPoolSize=1024)


def find_duplicate(collection):
    collection.aggregate([
        {'$group': {
            '_id': {'title': "$title", 'published': "$published", "link": "$link"},  # 去重字段
            'uniqueIds': {'$addToSet': "$_id"},  # 重复数据的id
            'count': {'$sum': 1}  # 重复次数
        }},
        {'$match': {
            'count': {'$gt': 1}  # 匹配重复次数大于1的数据
        }},
        {'$out': tmp_colName}  # 输出的表名
    ], allowDiskUse=True)


def del_dup(tmp_collection, source_collection):
    # 保留一位
    for a in tmp_collection.find():
        for b in a['uniqueIds'][1:]:
            source_collection.delete_one({"_id": b})
    tmp_col.drop()  # 删除中间表


if __name__ == '__main__':
    tmp_colName = "tmp_news"  # 中间表名
    col_list = ['caijing', 'ce', 'eastmoney', 'hexun', 'news', 'newsqq', 'sina', 'wangyi']
    for i in col_list:
        col = client['news'][i]
        tmp_col = client['news'][tmp_colName]
        find_duplicate(col)
        del_dup(tmp_col, col)
