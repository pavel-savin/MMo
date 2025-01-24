from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from my_HM.models import Subscription, Post

class Command(BaseCommand):
    help = 'Send weekly updates to subscribers'

    def handle(self, *args, **kwargs):
        last_week = now() - timedelta(days=7)
        for subscription in Subscription.objects.all():
            posts = Post.objects.filter(category=subscription.category, created_at__gte=last_week)
            if posts.exists():
                email_body = '\n'.join([f'{post.title}: http://127.0.0.1:8000/news/{post.id}' for post in posts])
                send_mail(
                    subject=f'Еженедельные обновления категории {subscription.category.name}',
                    message=email_body,
                    from_email='your_username@yandex.ru',
                    recipient_list=[subscription.user.email],
                )
