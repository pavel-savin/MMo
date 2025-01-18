from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# TODO: Сделать проверку на существование группы 'common'
# class BasicSignupForm(SignupForm):
#     def save(self, request):
#         # Сохраняем пользователя с помощью родительского метода
#         user = super(BasicSignupForm, self).save(request)
#         # Получаем группу 
#         basic_group = Group.objects.get(name='common')
#         # Добавляем пользователя в группу
#         basic_group.user_set.add(user)
#         return user
