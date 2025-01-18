from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from my_HM.models import Post
from django.views.generic import ListView

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
        common_group = Group.objects.get(name='common')  # Получаем группу common
        self.object.groups.add(common_group)  # Добавляем пользователя в группу
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


# Обновление пользователя до автора
@login_required
def upgrade_to_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


class PostsList(ListView):
    model = Post
    template_name = 'flatpages/default.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Проверяем, состоит ли пользователь в группе 'authors'
            is_author = self.request.user.groups.filter(name='authors').exists()
            print(f'Is user an author? {is_author}')  # Выводим информацию для отладки
            context['is_author'] = is_author
        else:
            context['is_author'] = False
        return context
