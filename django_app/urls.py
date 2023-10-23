from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register_page, name='register'),
    path('accounts/login/', views.login_page, name='login'),
    path('upload/', views.upload_json, name='upload_json'),
]