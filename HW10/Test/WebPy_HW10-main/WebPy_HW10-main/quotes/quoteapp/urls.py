from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import add_author, add_quote, AboutAuthorView


app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_author/', views.add_author, name='add_author'),
    path('author/<int:author_id>', views.author, name='author'),
    path('author/<int:author_id>/about/', AboutAuthorView.as_view(), name = 'about_author'),
]
