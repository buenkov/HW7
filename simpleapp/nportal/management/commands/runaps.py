import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils import timezone
from nportal.models import Post

logger = logging.getLogger(__name__)

def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(second="*/30"),
            #дайджест будем доставлять в субботу в 8 утра
            trigger=CronTrigger(day_of_week='sat', hour='8', minute='0'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")