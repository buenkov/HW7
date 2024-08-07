from django.urls import path
from .views import AnnouncementList, create_announcement, add_response, view_responses, create_news


urlpatterns = [
   path('add_response/<int:announcement_id>/', add_response, name='add_response'),
   path('', AnnouncementList.as_view(), name='announcement_list'),
   path('announcement_list', AnnouncementList.as_view(), name='announcement_list'),
   path('create/', create_announcement, name='create_announcement'),
   path('view_responses/', view_responses, name='view_responses'),
   path('create_news/', create_news, name='create_news'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
   # path('create/', ProductCreate.as_view(), name='product_create'),
   # path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   # path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   # path('redis/', IndexView.as_view()),
   # path('translate/', Translate.as_view()),
   # path('swagger/', TemplateView.as_view(
   #     template_name='swagger.html',
   #     extra_context={'schema_url':'openapi-schema'}
   # ), name='swagger'),
   # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]