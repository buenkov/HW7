from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Announcement, Response, News

class AnnouncmentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget, label='')

    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']  # Добавляем поле text
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отклик'}),
        }

class ResponseFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'Все'),
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, initial='all', label='Статус')
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Начальная дата')
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Конечная дата')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']