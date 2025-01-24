from django.contrib.auth.models import User
from my_HM.models import Author, Category, Post, PostCategory, Comment

# Создаем пользователей
user_1 = User.objects.create_user('user_111')
user_2 = User.objects.create_user('user_222')

# Создаем авторов
author_1 = Author.objects.create(user=user_1)
author_2 = Author.objects.create(user=user_2)

# Создаем категории
cate_1 = Category.objects.create(categories="Спорт")
cate_2 = Category.objects.create(categories="Искусство")
cate_3 = Category.objects.create(categories="Политика")
cate_4 = Category.objects.create(categories="Экономика")

# Создаем статьи и новости
article_1 = Post.objects.create(author=author_1, article_title_news="Заголовок статьи 1", text_title_news="Текст статьи 1")
article_2 = Post.objects.create(author=author_2, article_title_news="Заголовок статьи 2", text_title_news="Текст статьи 2")
news_1 = Post.objects.create(author=author_1, article_or_news=1, article_title_news="Заголовок новости 1", text_title_news="Текст новости 1")

# Присваиваем категории постам через промежуточную модель PostCategory
PostCategory.objects.create(post=article_1, category=cate_2)
PostCategory.objects.create(post=article_2, category=cate_1)
PostCategory.objects.create(post=article_2, category=cate_4)
PostCategory.objects.create(post=news_1, category=cate_3)

# Создаем комментарии
com_1 = Comment.objects.create(post=article_1, user=user_1, text="Текст комментария 1")
com_2 = Comment.objects.create(post=article_2, user=user_2, text="Текст комментария 2")
com_3 = Comment.objects.create(post=news_1, user=user_1, text="Текст комментария 3")
com_4 = Comment.objects.create(post=news_1, user=user_2, text="Текст комментария 4")

# Лайки и дизлайки постов и комментариев
article_1.like()
article_2.dislike()
news_1.dislike()
news_1.dislike()
com_1.like()
com_2.like()
com_1.like()
com_3.dislike()
com_4.dislike()

# Вывод лучшего пользователя по рейтингу
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, рейтинг: {best_author.rating}")

# Вывод лучшей статьи по рейтингу
best_post = Post.objects.order_by('-rating').first()
print(f"Лучшая статья: {best_post.article_title_news}, рейтинг: {best_post.rating}")

# Вывод комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f"Комментарий от {comment.user.username}: {comment.text}, рейтинг: {comment.rating}")
