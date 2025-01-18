from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .filter_search import PostFilter
from .forms import PostForm, ResponseForm
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Subscription, Post, Author, Response



# Список постов
class PostsList(ListView):
    model = Post
    ordering = '-automatic_data_time'
    template_name = 'flatpages/news_feed.html'
    context_object_name = 'Posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            # Получение категорий, на которые подписан пользователь
            subscribed_categories = Subscription.objects.filter(user=user).values_list('category_id', flat=True)
            context['subscribed_categories'] = subscribed_categories
        else:
            context['subscribed_categories'] = []
        return context




# Детали новости
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/Post.html'
    context_object_name = 'Post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # Получаем текущий пост

        # Получаем отклики для данного поста
        responses = post.responses.all().order_by('-created_at')  # Сортировка по убыванию
        context['responses'] = responses

        # Добавляем форму для нового отклика только для авторизованных пользователей
        if self.request.user.is_authenticated:
            context['form'] = ResponseForm()

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            # Сохраняем отклик
            response = form.save(commit=False)
            response.user = request.user
            response.post = post
            response.save()

            return HttpResponseRedirect(reverse('post_detail', args=[post.pk]))
        else:
            # Если форма не валидна, возвращаем на страницу с ошибками
            return self.get(request, *args, **kwargs)
   
   
# Поиск новостей    
class NewsSearchView(ListView):
    model = Post
    ordering = '-automatic_data_time'
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем фильтрацию, если есть параметры в запросе
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset  # Добавляем фильтр в контекст для отображения в шаблоне
        return context


    
# Переход после success_url
class BasePostView:
    success_url = reverse_lazy('posts_list')

    def get_success_url(self):
        return self.success_url


# Универсальный класс для создания, обновления и удаления постов
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    # Проверка на группу 'authors'
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.groups.filter(name='authors').exists():
    #         return HttpResponseForbidden("У вас нет прав на создание постов.")
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_success_url(self):
        return reverse_lazy('posts_list')  # Это перенаправит на список постов после успешного создания

    def form_valid(self, form):
        post = form.save(commit=False)
    
        # Получаем или создаем объект Author для текущего пользователя
        author, created = Author.objects.get_or_create(user=self.request.user)
    
        # Устанавливаем автора для поста
        post.author = author
    
        # Если путь начинается с /news/, то это новость, иначе статья
        if self.request.path.startswith('/news/'):
            post.article_or_news = 0  # новость
        elif self.request.path.startswith('/articles/'):
            post.article_or_news = 1  # статья

        # Сохраняем пост
        post.save()
    
        return super().form_valid(form)





class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    # Проверка на группу 'authors' и права на редактирование поста
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        # if not request.user.groups.filter(name='authors').exists():
        #     return HttpResponseForbidden("У вас нет прав на редактирование постов.")
        if post.author.user != request.user:
            return HttpResponseForbidden("Вы не можете редактировать чужие посты.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_success_url(self):
        return reverse_lazy('posts_list')  # Перенаправляем на список постов после успешного редактирования


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'

    # Проверка на группу 'authors'
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.groups.filter(name='authors').exists():
    #         return HttpResponseForbidden("У вас нет прав на удаление постов.")
    #     return super().dispatch(request, *args, **kwargs)

class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'flatpages/response_create.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        response.user = self.request.user
        response.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

    
class UserResponsesView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'flatpages/user_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        # Получаем отклики на посты, автором которых является текущий пользователь
        return Response.objects.filter(post__author__user=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        # Получаем отклик по его ID и обновляем статус
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')  # 'accept' или 'delete'
        response = get_object_or_404(Response, id=response_id)

        if action == 'accept':
            response.accepted = True
            response.save()
        elif action == 'delete':
            response.delete()

        # Перенаправляем обратно на страницу откликов
        return redirect('user_responses')
    
@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.get_or_create(user=request.user, category=category)

    # Получение URL для возврата
    next_url = request.GET.get('next', 'posts_list')
    return redirect(next_url)

@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.filter(user=request.user, category=category).delete()

    # Получение URL для возврата
    next_url = request.GET.get('next', 'posts_list')
    return redirect(next_url)



# # Универсальный класс для создания, обновления и удаления постов
# class PostCreateView(BasePostView, CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'flatpages/post_edit.html'
    
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         # Устанавливаем тип в зависимости от URL
#         if 'news' in self.request.path:
#             post.article_or_news = 0  # новость
#         elif 'articles' in self.request.path:
#             post.article_or_news = 1  # статья
#         return super().form_valid(form)

# class PostUpdateView(BasePostView, UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'flatpages/post_edit.html'

# class PostDeleteView(BasePostView, DeleteView):
#     model = Post
#     template_name = 'flatpages/post_delete.html'