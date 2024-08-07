from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Product
       fields = ['id', 'name', 'description', ]



class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name', ]

