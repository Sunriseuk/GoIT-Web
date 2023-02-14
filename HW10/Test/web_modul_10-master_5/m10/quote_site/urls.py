from . import views
from django.urls import path

app_name = 'quote_site'
urlpatterns = [
    path("", views.index, name="index"),
    path('<int:id>/', views.author_detail, name='author_detail'),
    path('add_author', views.add_author, name="add_author"),
    path('add_quote', views.add_quote, name="add_quote")
]
