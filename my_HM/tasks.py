from celery import shared_task
from .models import Subscription, Post
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = Subscription.objects.filter(category__in=post.post_category.all())

    for subscriber in subscribers:
        send_mail(
            f'Новость: {post.article_title_news}',
            f'Новая новость: {post.text_title_news}\nЧитать полностью: {post.get_absolute_url()}',
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.user.email]
        )
        
@shared_task
def send_weekly_newsletter():
    from datetime import timedelta
    from django.utils import timezone
    from django.core.mail import send_mail

    # Получаем все новости за последнюю неделю
    one_week_ago = timezone.now() - timedelta(weeks=1)
    posts = Post.objects.filter(pub_date__gte=one_week_ago)

    # Получаем все email подписчиков
    subscribers = Subscription.objects.filter(category__in=[post.post_category.all() for post in posts]).values_list('user__email', flat=True).distinct()

    # Создаем письмо
    subject = 'Еженедельная рассылка новостей'
    message = 'Вот новости за последнюю неделю:\n\n'

    for post in posts:
        message += f'{post.article_title_news} - {post.get_absolute_url()}\n'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        list(subscribers)
    )

