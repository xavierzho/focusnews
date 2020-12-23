"""
@Author: Jonescyna@gmail.com
@Created: 2020/12/23
"""
import os
import logging
import time
from multiprocessing import Process
from scrapy import cmdline
from .celery import app


# 获取爬虫列表
def _get_spider_list():
    return [i for i in os.popen('scrapy list').read().split('\n') if i]


@app.task
def start_spider():
    args = 'scrapy crawl %s'

    target_list = [Process(target=cmdline.execute, args=(args % i,)) for i in _get_spider_list()]
    for target in target_list:
        start_time = time.localtime()
        target.start()
        target.join()
        target.run()
        logging.debug(f'### start_time:{time.strftime("%Y-%m-%d %H:%M:%S",start_time)} use_time:{time.time() - time.mktime(start_time)} end_time:{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}')
