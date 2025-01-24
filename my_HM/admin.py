from django.contrib import admin
from .models import *
from .forms import PostForm

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscription)
admin.site.register(Response)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('article_title_news', 'automatic_data_time', 'rating')

# Register your models here.
