from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscription)
admin.site.register(Response)
admin.site.register(Video)

# Register your models here.
