from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    #Так можно описать условие дляны описания на форме
    class Meta:
       model = Post
       fields = [
           'author',
           'title',
           'text',
           'categories',
       ]