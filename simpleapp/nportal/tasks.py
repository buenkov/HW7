from celery import shared_task
from celery.contrib import rdb
import time
from .models import Post
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def sender_subsribers(pid):
    print('Начинаю отправку сообщений')
    instance = Post.objects.get(id = pid)
    if instance.art_new == 'N':
        subscribe_group = Group.objects.get(name='sub_N')
        users = subscribe_group.user_set.all()
        link = f'http://127.0.0.1:8000/portal/{instance.id}',
        for user in users:
            email = tuple(user.email.split('  '))
            username = user.username
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {username}, Создана новая новость с темой: {instance.title}',
                body=f'Здравствуй, {username}, Новая статья в твоём любимом разделе!  {instance.text}',
                # это то же, что и message
                from_email='buenkov-ta@yandex.ru',
                to=email,  # это то же, что и recipients_list
            )

            html_content = render_to_string(
                'post_created.html',
                {
                    'username': username,
                    'post': instance,
                    'link':link,
                }
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            rdb.set_trace()
            msg.send()  # отсылаем
