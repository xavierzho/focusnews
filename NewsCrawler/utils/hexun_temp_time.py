import time

origin_temp_time = 53537171

start = time.mktime(time.strptime('2020-11-23 07:04:34', '%Y-%m-%d %H:%M:%S'))

temp_time = (time.time() - start - 28800) // 30 + origin_temp_time
