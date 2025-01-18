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


# Уведомление подписчиков при добавлении поста
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Отправляем письмо только при создании нового пользователя
        
        # Генерация токена для подтверждения email
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(str(instance.pk).encode())
        
        # Получаем текущий домен для формирования URL
        domain = get_current_site(None).domain
        # Используйте правильный путь для подтверждения почты
        path = reverse('account:email_verification', kwargs={'uidb64': uid, 'token': token})  # Убедитесь, что у вас есть этот путь
        confirm_url = f'http://{domain}{path}'

        # Формируем сообщение с приветствием и подтверждением
        subject = 'Добро пожаловать на наш сайт!'

        message = f"""
        Здравствуйте, {instance.username}!

        Спасибо за регистрацию на нашем сайте!

        Для завершения регистрации и подтверждения вашей электронной почты, пожалуйста, перейдите по следующей ссылке:

        {confirm_url}

        Если вы не регистрировались на сайте, просто проигнорируйте это письмо.

        С уважением,
        Ваша команда!
        """

        send_email(
            subject=subject,
            message=message,
            recipient_list=[instance.email],
        )

@receiver(post_save, sender=Response)
def notify_user_on_acceptance(sender, instance, created, **kwargs):
    if not created and instance.status == 'accepted':  # например, статус отклика 'accepted'
        send_email(
            subject='Ваш отклик принят!',
            message=f'Ваш отклик на объявление "{instance.post.article_title_news}" принят.',
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
    if created:
        send_email(
            subject='Ваше объявление в категории',
            message=f'Ваше объявление "{instance.article_title_news}" размещено в категории: {", ".join(instance.post_category.values_list("name", flat=True))}.',
            recipient_list=[instance.author.user.email],
        )

# Уведомление об откликах через Celery
@receiver(post_save, sender=Response)
def notify_author_on_response(sender, instance, created, **kwargs):
    if created:
        # Отправляем уведомление автору поста
        send_email(
            subject='Новый отклик на ваше объявление',
            message=f'На ваше объявление "{instance.post.article_title_news}" поступил отклик:\n\n{instance.text}',
            recipient_list=[instance.post.author.user.email],
        )
