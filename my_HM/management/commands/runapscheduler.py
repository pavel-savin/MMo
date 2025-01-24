import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from my_HM.models import User, Subscription, Post  # Замените `myapp` на имя вашего приложения

logger = logging.getLogger(__name__)

# Задача для рассылки новых статей
def send_weekly_articles():
    logger.info("Starting weekly article distribution...")
    last_week = now() - timedelta(days=7)

    # Получаем всех пользователей с активными подписками
    users = User.objects.filter(subscription__isnull=False).distinct()

    for user in users:
        # Находим категории, на которые подписан пользователь
        subscribed_categories = Subscription.objects.filter(user=user).values_list('category', flat=True)
        
        # Выбираем новые статьи за последнюю неделю из этих категорий
        articles = Post.objects.filter(
            post_category__in=subscribed_categories,
            automatic_data_time__gte=last_week
        ).distinct()

        if articles.exists():
            # Формируем список ссылок на статьи
            article_links = "\n".join(
                [f"{article.article_title_news}: {article.preview()}" for article in articles]
            )

            # Отправляем email
            send_mail(
                subject="Новые статьи за неделю",
                message=f"Привет, {user.username}!\n\nВот новые статьи за последнюю неделю:\n\n{article_links}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

    logger.info("Weekly article distribution completed.")

# Функция для удаления устаревших задач
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу рассылки статей
        scheduler.add_job(
            send_weekly_articles,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),  # Каждую неделю в понедельник в 8 утра
            id="send_weekly_articles",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_articles'.")

        # Добавляем задачу удаления устаревших задач
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
