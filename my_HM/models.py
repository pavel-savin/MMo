from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

Tanks = 'TN'
Healers = 'HL'
DD = 'DD'
Trader = 'ME'
GuildMasters = 'GM'
QuestGivers = 'QG'
Blacksmiths = 'BS'
Tanners = 'TS'
PotionMakers = 'PM'
SpellMasters = 'SM'



class Author(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    rating = models.IntegerField(default=0)
   
    def __str__(self):
        return self.user.username
    
    
class Category(models.Model):
    categories = models.CharField(max_length=100, unique=True)
    CATEGORYES = [
    (Tanks, 'Танки'),
    (DD, 'ДД'),
    (Healers, 'Хиллеры'),
    (Trader, 'Торговцы'),
    (GuildMasters, 'Гилдмастера'),
    (QuestGivers, 'Квестгиверы'),
    (Blacksmiths, 'Кузнецы'),
    (Tanners, 'Кожевники'),
    (PotionMakers, 'Зельевары'),
    (SpellMasters, 'Мастера заклинаний'),
    ]
    category_type = models.CharField(max_length=20, choices=CATEGORYES, default=Tanks)
    
    def __str__(self):
        return self.categories
    


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    article_or_news = models.IntegerField(default= 0)
    automatic_data_time = models.DateTimeField(auto_now_add= True)
    post_category = models.ManyToManyField(Category, through= 'PostCategory')
    article_title_news = models.CharField(max_length= 255, db_index=True) #добавлено индексирование
    text_title_news = models.TextField()
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
     
    def preview(self):
        return f"{self.text_title_news[:124]}..."
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return super().__str__() + f' {self.category.categories}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    automatic_data_time = models.DateTimeField(auto_now_add= True)
    rating = models.IntegerField(default=0)
    

        
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')
        

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField(verbose_name='Текст отклика')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, verbose_name='Принят')

    def __str__(self):
        return f'Отклик от {self.user.username} на "{self.post.article_title_news}"'

    def accept(self):
        self.accepted = True
        self.save()

    def delete(self):
        super().delete()
