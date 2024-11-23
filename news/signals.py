import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from .models import PostCategory, Post
from django.template.loader import render_to_string

from .tasks import send_email_task


def send_notifications(preview, pk, header, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )


    msg.attach_alternative(html_content, 'text/html')
    msg.send()




@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_email_task.delay(instance.pk)


#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(sender, instance, **kwargs):
#    if kwargs['action'] == 'post_add':
#       categories = instance.category.all()
#       subscribers_emails = []

#       for cat in categories:
#           subscribers = cat.subscribers.all()
#          subscribers_emails += [s.email for s in subscribers]
#
#       send_notifications(instance.preview(), instance.pk, instance.header, subscribers_emails)


#@receiver(pre_save, sender=Post)
#def post_limit(sender, instance, **kwargs):
#    today = datetime.date.today()
#    post_limit = Post.objects.filter(author=instance.author, create_time__date=today).count()
#    if post_limit >= 3:
#        raise ValidationError('Нельзя публиковать больше трех постов в сутки!!!')