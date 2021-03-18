"""
@Author: Jonescyna@gmail.com
@Created: 2020/12/29
"""
from scrapy.cmdline import execute
from multiprocessing import Pool

spider_list = ['caijing', 'ce', 'eastmoney', 'hexun', 'news', 'newsqq', 'sina', 'wangyi']


def run_spider(spider_name):
    execute(['scrapy', 'crawl', spider_name])


if __name__ == '__main__':
    pool = Pool(10)

    for spider in spider_list:

        pool.apply_async(run_spider, args=(spider,))
    pool.close()
    pool.join()

