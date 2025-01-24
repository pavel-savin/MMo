from django.contrib.auth.models import User
from django.db import models
from random import randint
import datetime

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)

    @staticmethod
    def generate_activation_code(user):
        """Генерация и сохранение кода активации для пользователя."""
        code = str(randint(10000, 99999))
        Profile.objects.create(user=user, code=code, date=datetime.date.today())
        return code
