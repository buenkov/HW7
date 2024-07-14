from django import template
from nportal.models import *


register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   # получаем список всех плохих слов из БД
   titles = BadWords.objects.all().values('title').values_list('title', flat=True)
   words =value.split()
   S = ""
   for word in words:
      if word.lower() in titles:
         # берем первую букву
         _word = word[0]
         _lword = word[-1]
         # далее столько звездочек, сколько букв
         word = _word + ("*" *(len(word)-2)) + _lword
      S += word + " "
   # Убираем лищний пробел
   return S[:-1]

@register.filter
def pow(value, exponent):
    return value ** exponent


