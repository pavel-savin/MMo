from django.urls import path
from .views import (
    PostsList, PostDetail, NewsSearchView, PostCreateView, PostUpdateView, PostDeleteView, ResponseCreateView, UserResponsesView
) 
from .views import subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),  # Главная страница с постами
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),  # Страница деталей поста
    path('search/', NewsSearchView.as_view(), name='news_search'),
    
    path('create/', PostCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    
    path('create/', PostCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
    
    path('category/<int:category_id>/subscribe/', 
        subscribe_to_category, name='subscribe_to_category'),
    path('category/<int:category_id>/unsubscribe/', 
        unsubscribe_from_category, name='unsubscribe_from_category'),
    
    path('post/<int:pk>/respond/', ResponseCreateView.as_view(), name='create_response'),
    path('responses/', UserResponsesView.as_view(), name='user_responses'),
]
