from django import forms
from .models import Post, Subscription, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_category', 'article_title_news', 'text_title_news', 'image']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['category']
        
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Введите текст отклика', 'rows': 4}),
        }