from django.urls import path
from .views import PostsList, PostDetail, create_post, PostCreate, PostUpdate, PostDelete, NewsList, ArticlesList, \
   subscribe_news, subscribe_arts

urlpatterns = [
    # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('news/subscribeN/', subscribe_news, name='subscribe_news'),
   path('articles/subscribeN/', subscribe_arts, name='subscribe_arts'),
]