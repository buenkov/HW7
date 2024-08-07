from django.urls import path, include
from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, IndexView, Translate
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewset)
router.register(r'category', views.CategorytViewset)

urlpatterns = [
    # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', include(router.urls)),
   path('all', ProductsList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('redis/', IndexView.as_view()),
   path('translate/', Translate.as_view()),
   path('swagger/', TemplateView.as_view(
       template_name='swagger.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger'),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]