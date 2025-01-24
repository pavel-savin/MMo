from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Subscription, User, Response
from .tasks import send_post_notification  # Celery task 
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from celery import shared_task


# Общая функция для отправки писем
def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email='BangBong097@yandex.ru',
        recipient_list=recipient_list,
    )


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response

@receiver(post_save, sender=Response)
def notify_user_on_accept(sender, instance, created, **kwargs):
    # Проверяем, что это не создание, а изменение отклика
    if not created and instance.accepted:
        # Уведомление пользователю, который оставил отклик
        send_email(
            subject='Ваш отклик был принят',
            message=(
                f'Ваш отклик на объявление "{instance.post.article_title_news}" был принят!\n\n'
                f'Текст отклика: {instance.text}\n\n'
                f'Автор объявления: {instance.post.author.user.username}'
            ),
            recipient_list=[instance.user.email],
        )


@shared_task
def send_reminder_for_response_filtering():
    users = User.objects.filter(response__isnull=False)
    for user in users:
        send_email(
            subject='Напоминание о фильтрации откликов',
            message='Не забудьте фильтровать или принимать отклики на ваши объявления!',
            recipient_list=[user.email],
        )

@receiver(post_save, sender=Post)
def notify_category(sender, instance, created, **kwargs):
    print(f"{created}")
    if created:
        send_email(
            subject='Ваше объявление в категории',
            message=f'Ваше объявление "{instance.article_title_news}" размещено в категории: {", ".join(instance.post_category.values_list("categories", flat=True))}.',
            recipient_list=[instance.author.user.email],
        )

# Уведомление об откликах
@receiver(post_save, sender=Response)
def notify_author_on_response(sender, instance, created, **kwargs):
    if created:
        # Отправляем уведомление автору поста
        send_email(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление "{instance.post.article_title_news}" поступил отклик:\n\n{instance.text}',
            recipient_list=[instance.post.author.user.email],
        )
