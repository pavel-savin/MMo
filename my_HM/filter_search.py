import django_filters
from .models import Post, Category
from django import forms

class PostFilter(django_filters.FilterSet):
    article_title_news = django_filters.CharFilter(
        lookup_expr='icontains', label='Название'
    )
    author__user__username = django_filters.CharFilter(
        lookup_expr='icontains', label='Автор'
    )
    automatic_data_time = django_filters.DateFilter(
        lookup_expr='gte', label='Поле даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Можно использовать выпадающий список, если нужно
        label='Категория',
        field_name='post_category'  # Используем поле Many-to-Many напрямую
    )

    class Meta:
        model = Post
        fields = ['article_title_news', 'author__user__username', 'automatic_data_time', 'category']
