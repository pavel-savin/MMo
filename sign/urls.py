from django.urls import path
from django.contrib.auth.views import LoginView
from . import views  # Импортируем views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('signup/', views.BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('confirm_logout/', views.confirm_logout, name='confirm_logout'),  # Подтверждение выхода
    path('logout/', views.logout_view, name='logout'),  # Основной выход
    path('upgrade_to_author/', views.upgrade_to_author, name='upgrade_to_author'),
]
