from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BasicSignupForm(SignupForm):
    def save(self, request):
        # Сохраняем пользователя с помощью родительского метода
        user = super(BasicSignupForm, self).save(request)
        return user
