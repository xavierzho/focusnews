"""
@Author: Jonescyna@gmail.com
@Created: 2020/12/23
"""
import os

import celery
from celery.schedules import crontab

backend = os.getenv("redisURI") + "/0"
broker = os.getenv("redisURI") + "/0"
app = celery.Celery(__name__, backend=backend, broker=broker, include=[])

# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 任务的定时配置

app.conf.beat_schedule = {
    'start_spider': {
        'task': 'celery_task.run_spider',
        'schedule': crontab(hour=0, minute=10),  # 每天24点爬取
    }
}
