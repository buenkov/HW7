from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tasks import sender_subsribers

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель

# Комментируем сигнал, будем отправлять из celery

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    sender_subsribers.apply_async([instance.id], countdown=5)

    # if instance.art_new == 'N':
    #
    #     subscribe_group = Group.objects.get(name='sub_N')
    #     users = subscribe_group.user_set.all()
    #     link = f'http://127.0.0.1:8000/portal/{instance.id}',
    #     for user in users:
    #         email = tuple(user.email.split('  '))
    #         username = user.username
    #         msg = EmailMultiAlternatives(
    #             subject=f'Здравствуй, {username}, Создана новая новость с темой: {instance.title}',
    #             body=f'Здравствуй, {username}, Новая статья в твоём любимом разделе!  {instance.text}',
    #             # это то же, что и message
    #             from_email='buenkov-ta@yandex.ru',
    #             to=email,  # это то же, что и recipients_list
    #         )
    #
    #         html_content = render_to_string(
    #             'post_created.html',
    #             {
    #                 'username': username,
    #                 'post': instance,
    #                 'link':link,
    #             }
    #         )
    #         msg.attach_alternative(html_content, "text/html")  # добавляем html
    #         msg.send()  # отсылаем
    # if instance.art_new == 'A':
    #
    #     subscribe_group = Group.objects.get(name='sub_A')
    #     users = subscribe_group.user_set.all()
    #     link = f'http://127.0.0.1:8000/portal/{instance.id}',
    #     for user in users:
    #         email = tuple(user.email.split('  '))
    #         username = user.username
    #         msg = EmailMultiAlternatives(
    #             subject=f'Создана новая статья с темой: {instance.title}',
    #             body=f'Здравствуй, {username}, Новая статья в твоём любимом разделе!  {instance.text}',
    #             # это то же, что и message
    #             from_email='buenkov-ta@yandex.ru',
    #             to=email,  # это то же, что и recipients_list
    #         )
    #
    #         html_content = render_to_string(
    #             'post_created.html',
    #             {
    #                 'username': username,
    #                 'post': instance,
    #                 'link': link,
    #             }
    #         )
    #         msg.attach_alternative(html_content, "text/html")  # добавляем html
    #         msg.send()  # отсылаем