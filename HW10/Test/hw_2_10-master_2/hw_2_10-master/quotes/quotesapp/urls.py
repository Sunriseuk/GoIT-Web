from django.urls import path
from . import views
from .views import AuthorPage

app_name = 'quotesapp'


urlpatterns = [
    path('', views.main, name='main'),
    path('addtag/', views.addtag, name='addtag'),
    path('addauthor/', views.addauthor, name='addauthor'),
    path('addquote/', views.addqoute, name='addquote'),
    path("author/<str:fullname>", AuthorPage.as_view(), name="author"),
]
