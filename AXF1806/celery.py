from  __future__ import absolute_import
import os
from celery import Celery

from django.conf import settings

os.environ.setdefault("DJANGO_SETTING_MODULE", "AXF1806.settings")
app = Celery('mycelery')
app.conf.CELERY_TIMEZONE = "Asia/Shanghai"
app.config_from_object("django.conf:settings")
#让celery 自动去发现我们的任务（task）
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS) #你需要在app目录下 新建一个叫tasks.py（一定不要写错）文件