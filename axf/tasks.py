from  celery import task
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from  django.core.cache import caches
cache = caches['confirm']

@task
def send_verify_mail(url, user_id , receiver):
    title = "爱鲜蜂验证测试"
    content = ''
    template = loader.get_template('mine/email.html')
    html = template.render({"url":url})
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(title,content,email_from,[receiver],html_message=html)
    cache.set(url.split('/')[-1],user_id,60*60)

