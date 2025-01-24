from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_HM.models import Post
from django.views.generic import ListView
from allauth.account.forms import  SignupForm

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
    success_url = '/'
     
    def form_valid(self, form):
        response = super().form_valid(form)  # Сохраняем пользователя
        return response


# Подтверждение выхода
def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')


# Основной выход
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/news/')
    return redirect('confirm_logout')

class PostsList(ListView):
    model = Post
    template_name = 'flatpages/default.html'
    context_object_name = 'posts'
