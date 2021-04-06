"""
@Author: Jonescyna@gmail.com
@Created: 2021/3/18
"""
import datetime

from dateutil.parser import parse

test_list = ["2021/3/18",
             "2020-12-29 10:40:12",
             "2020-12-28 10:20",
             "2020-12-29 10",
             '03-18 13:27',
             "2021年03月18日 10:48"
             ]


def validate_replace(published: str) -> str:
    """
    验证时间格式并替换,如果为空返回时间是0，所以加上当前时间为新的时间
    :param published:
    :return:
    """
    res = parse(published)

    if res.hour == 0:
        res = res + datetime.timedelta(hours=datetime.datetime.now().hour)
    if res.minute == 0:
        res = res + datetime.timedelta(minutes=datetime.datetime.now().minute)
    if res.second == 0:
        res = res + datetime.timedelta(seconds=datetime.datetime.now().second)
    return res.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    for test in test_list:
        print(validate_replace(test))
    # validate_published()
