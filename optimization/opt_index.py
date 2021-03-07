"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/9
"""
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017", maxPoolSize=1024)
# coll_list = ["caijing", 'ce', 'eastmoney', 'hexun', 'news', 'newsqq', 'sina', 'wangyi']
# for coll in coll_list:
#     conn = client["news"][coll]
#     conn
conn = client['test']['test']
for i in conn.find():

    conn.update_one({"_id": i["_id"]}, {"$set": {"_id": i['published'].strftime("%Y%m%d%H%M%S")}})
# conn.update_many({}, {"$rename": {"time": "published"}})  # 修改列名
