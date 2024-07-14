
from django.contrib import admin
from .models import Post, BadWords

class PostAdmin(admin.ModelAdmin):

    # напишем уже знакомую нам функцию обнуления товара на складе
    def change_type(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
        queryset.update(art_new='N')

    change_type.short_description = 'Сделать новостью'  # описание для более понятного представления в админ панеле задаётся, как будто это объект

    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    list_display = ('create_date', 'author', 'title', 'art_new','is_news')  # оставляем только имя и цену товара
    list_filter = ('create_date', 'author', 'title', 'art_new')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text') # тут всё очень похоже на фильтры из запросов в базу
    actions = [change_type]  # добавляем действия в список
admin.site.register(Post, PostAdmin)
admin.site.register(BadWords)