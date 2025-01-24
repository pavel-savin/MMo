
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_HM.models import Post
from django.views.generic import ListView
from allauth.account.forms import SignupForm
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

# Встроенная форма регистрации
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# Представление для регистрации
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/activation/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Отключаем пользователя до активации
        user.save()

        # Генерация кода активации
        code = Profile.generate_activation_code(user)

        # Отправка письма с кодом
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


# Подтверждение выхода
def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')


# Основной выход
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/news/')
    return redirect('confirm_logout')


# Активация пользователя
def activation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            # Проверяем, существует ли профиль с указанным кодом
            profile = Profile.objects.get(code=code, user__is_active=False)
            profile.user.is_active = True
            profile.user.save()
            profile.delete()  # Удаляем профиль после успешной активации

            # Указываем бэкенд аутентификации
            profile.user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, profile.user)

            return redirect('/sign/login/')  # Перенаправление после активации
        except Profile.DoesNotExist:
            return render(request, 'sign/activate.html', {'error': 'Неверный код активации или пользователь уже активирован'})
    
    return render(request, 'sign/activate.html')
