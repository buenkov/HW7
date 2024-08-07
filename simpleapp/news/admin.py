from django.contrib import admin
from .models import Category, Product
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

class CategoryAdmin(TranslationAdmin):
    model = Category

class ProductAdmin(TranslationAdmin):
    model = Product

admin.site.register(Category)
admin.site.register(Product)

# Register your models here.