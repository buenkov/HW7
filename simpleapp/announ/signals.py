from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response

@receiver(post_save, sender=Response)
def send_notification_to_author(sender, instance, created, **kwargs):
    if created:
        announcement = instance.announcement_id
        author = announcement.author.user
        send_mail(
            subject=f'Новый отклик на ваше объявление "{announcement.title}"',
            message=f'Пользователь {instance.player_id.user.username} откликнулся на ваше объявление "{announcement.title}".',
            from_email='buenkov-ta@yandex.ru',
            recipient_list=[author.email],
            fail_silently=False,
        )

@receiver(pre_save, sender=Response)
def notify_response_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous_response = Response.objects.get(pk=instance.pk)
        if previous_response.status != instance.status:
            announcement = instance.announcement_id
            player = instance.player_id.user
            send_mail(
                subject=f'Статус вашего отклика изменен на "{announcement.title}"',
                message=f'Статус вашего отклика на объявление "{announcement.title}" изменен на "{instance.get_status_display()}".',
                from_email='buenkov-ta@yandex.ru',  # замените на ваш email
                recipient_list=[player.email],
                fail_silently=False,
            )