from datetime import timezone
from celery import shared_task
import time
from django.conf import settings
from django.template.loader import render_to_string
import datetime
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Post, Category
import logging

logger = logging.getLogger(__name__)

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")
@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    header = post.post_header
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)


    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.post_header}',
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )


    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(create_time__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))


    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )


    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()




#celery -A NewsPaper worker -l INFO --pool=solo
#celery -A NewsPaper beat -l INFO
#python manage.py runserver 8002
#venv\scripts\activate
#--concurrency=10