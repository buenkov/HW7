from celery import shared_task
from .models import Post
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils import timezone

@shared_task
def sender_subsribers(pid):
    print('Начинаю отправку сообщений')
    instance = Post.objects.get(pk = pid)
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
            msg.send()  # отсылаем
    if instance.art_new == 'A':
        subscribe_group = Group.objects.get(name='sub_A')
        users = subscribe_group.user_set.all()
        link = f'http://127.0.0.1:8000/portal/{instance.id}',
        for user in users:
            email = tuple(user.email.split('  '))
            username = user.username
            msg = EmailMultiAlternatives(
                subject=f'Создана новая статья с темой: {instance.title}',
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
                    'link': link,
                }
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем

@shared_task
def weakly_report():
    #  Your job processing logic here...
    print('Начинаем отправку еженедельной рассылки новостей')
    subscribe_group = Group.objects.get(name='sub_N')
    users = subscribe_group.user_set.all()
    today = timezone.now() - timedelta(days=8)
    posts = Post.objects.filter(create_date__gt=today, art_new='N')
    for user in users:
        email = tuple(user.email.split('  '))
        username = user.username
        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {username}, Получите пожалуйста ваш еженедельный дайджест новостей',
            body=f'Здравствуй, {username}',
            # это то же, что и message
            from_email='buenkov-ta@yandex.ru',
            to=email,  # это то же, что и recipients_list
        )

        html_content = render_to_string(
            'post_mailing.html',
            {
                'username': username,
                'posts': posts,
            }
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

    print('Начинаем отправку еженедельной рассылки статей')
    subscribe_group = Group.objects.get(name='sub_A')
    users = subscribe_group.user_set.all()
    today = timezone.now() - timedelta(days=8)
    posts = Post.objects.filter(create_date__gt=today, art_new='A')
    for user in users:
        email = tuple(user.email.split('  '))
        username = user.username
        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {username}, Получите пожалуйста ваш еженедельный дайджест статей',
            body=f'Здравствуй, {username}',
            # это то же, что и message
            from_email='buenkov-ta@yandex.ru',
            to=email,  # это то же, что и recipients_list
        )

        html_content = render_to_string(
            'post_mailing.html',
            {
                'username': username,
                'posts': posts,
            }
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем