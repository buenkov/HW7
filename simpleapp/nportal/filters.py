import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class DateInput(forms.DateInput):
    input_type = 'date'
class PostFilter(FilterSet):
    # Создаем тип поля календарь
    create_date = django_filters.DateFilter(
        field_name='create_date',
        label='Дата создания позже',
        widget=DateInput(attrs={'class': 'datepicker'}),
        lookup_expr='gte',
    )
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию заголовка
           'title': ['icontains'],
           # поиск по имени автора
           'author': ['exact'],
           # дата создания должна быть позже
           #'create_date': ['gte'],
       }