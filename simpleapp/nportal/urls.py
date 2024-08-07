"""
This module defines URL patterns for your Django application.
"""

from django.urls import path, include
from .views import PostsList, PostDetail, PostCreate
from .views import PostUpdate, PostDelete, NewsList, ArticlesList
from .views import subscribe_news, subscribe_arts
#from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'new', views.NewsViewset, basename='news')
router.register(r'arts', views.ArtViewset, basename='art')



urlpatterns = [
    # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # Кэшируем страницу с новостями на 1 минуту.
   #path('', cache_page(60*10)(PostsList.as_view()), name='post_list'),
   path('', include(router.urls)),
   path('all', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', ArticlesList.as_view(), name='articles_list'),
   # Кэшируем детальную страницу поста на 5 минут.
   #path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('news/subscribeN/', subscribe_news, name='subscribe_news'),
   path('articles/subscribeN/', subscribe_arts, name='subscribe_arts'),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
